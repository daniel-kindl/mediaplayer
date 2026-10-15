#!/usr/bin/env python3
"""Map packaged VLC modules to source and contrib component candidates.

The TSV contains a union of conditional source and recipe branches. It does not
identify an exact link graph for a platform. Build dependencies can include tools
and header inputs. Source license grants do not establish redistribution clearance.
Bundled sources, such as GnuTLS's included libtasn1 and unistring, need a separate
review within their parent source archive. Unknown grants and Make expressions
need manual review. The output does not execute native code or use the network.
"""

import argparse
import collections
import csv
import pathlib
import re
import sys

VARIABLE_ALIASES = {
    'AOM': 'aom',
    'ARCHIVE': 'libarchive',
    'ARIBB24': 'aribb24',
    'ARIBB25': 'aribb25',
    'ASDCP': 'asdcplib',
    'AVCODEC': 'ffmpeg',
    'AVFORMAT': 'ffmpeg',
    'AVUTIL': 'ffmpeg',
    'BLURAY': 'bluray',
    'BPG': 'bpg',
    'CACA': 'caca',
    'CDDB': 'cddb',
    'CHROMAPRINT': 'chromaprint',
    'CHROMECAST': 'protobuf',
    'DAV1D': 'dav1d',
    'DCA': 'dca',
    'DSM': 'libdsm',
    'DVBPSI': 'dvbpsi',
    'DVDCSS': 'dvdcss',
    'DVDNAV': 'dvdnav',
    'DVDREAD': 'dvdread',
    'FAAD': 'faad2',
    'FLAC': 'flac',
    'FLUIDLITE': 'fluidlite',
    'FLUIDSYNTH': 'fluid',
    'FONTCONFIG': 'fontconfig',
    'FREETYPE': 'freetype2',
    'FRIBIDI': 'fribidi',
    'GCRYPT': 'gcrypt',
    'GNUTLS': 'gnutls',
    'GOOM': 'goom',
    'HARFBUZZ': 'harfbuzz',
    'JPEG': 'jpeg',
    'KATE': 'kate',
    'LIBARCHIVE': 'libarchive',
    'LIBASS': 'ass',
    'LIBCDDB': 'cddb',
    'LIBDSM': 'libdsm',
    'LIBDVDCSS': 'dvdcss',
    'LIBGCRYPT': 'gcrypt',
    'LIBPLACEBO': 'libplacebo',
    'LIBRIST': 'librist',
    'LIBS_a52': 'a52',
    'LIBS_crystalhd': 'crystalhd',
    'LIBS_faad': 'faad2',
    'LIBS_fluidsynth': 'fluid',
    'LIBS_freetype': 'freetype2',
    'LIBS_gme': 'gme',
    'LIBS_libass': 'ass',
    'LIBS_live555': 'live555',
    'LIBS_mkv': 'matroska',
    'LIBS_mod': 'modplug',
    'LIBS_x264': 'x264',
    'LIBS_x26410b': 'x264',
    'LIBVORBIS': 'vorbis',
    'LIBXML2': 'libxml2',
    'LUA': 'lua',
    'MAD': 'mad',
    'MICRODNS': 'microdns',
    'MPC': 'mpcdec',
    'MPCDEC': 'mpcdec',
    'MPEG2': 'libmpeg2',
    'MPG123': 'mpg123',
    'NFS': 'nfs',
    'OGG': 'ogg',
    'OGGSPOTS': 'ogg',
    'OPUS': 'opus',
    'PNG': 'png',
    'PROJECTM': 'projectM',
    'SAMPLERATE': 'samplerate',
    'SDL': 'sdl',
    'SDL_IMAGE': 'SDL_image',
    'SFTP': 'ssh2',
    'SHOUT': 'shout',
    'SMB2': 'smb2',
    'SMBCLIENT': None,
    'SOXR': 'soxr',
    'SPATIALAUDIO': 'spatialaudio',
    'SPEEX': 'speex',
    'SPEEXDSP': 'speexdsp',
    'SRT': 'srt',
    'SWSCALE': 'ffmpeg',
    'TAGLIB': 'taglib',
    'THEORA': 'theora',
    'TIGER': 'tiger',
    'TWOLAME': 'twolame',
    'UPNP': 'upnp',
    'VNC': 'vncclient',
    'VNC_CLIENT': 'vncclient',
    'VORBIS': 'vorbis',
    'VPL': 'vpl',
    'VPX': 'vpx',
    'XML': 'libxml2',
    'ZLIB': 'zlib',
    'ZVBI': 'zvbi',
}

HEADER_PATTERNS = [
    ('^libav(?:codec|format|util)/|^libswscale/', 'ffmpeg'),
    ('^gnutls/', 'gnutls'),
    ('^gcrypt\\.h$', 'gcrypt'),
    ('^gpg-error\\.h$', 'gpg-error'),
    ('^ft2build\\.h$|^freetype/', 'freetype2'),
    ('^fontconfig/', 'fontconfig'),
    ('^fribidi/|^fribidi\\.h$', 'fribidi'),
    ('^hb(?:-ft|-ot|-version)?\\.h$', 'harfbuzz'),
    ('^ass/', 'ass'),
    ('^zlib\\.h$', 'zlib'),
    ('^png\\.h$', 'png'),
    ('^jpeglib\\.h$', 'jpeg'),
    ('^archive(?:_entry)?\\.h$', 'libarchive'),
    ('^ogg/', 'ogg'),
    ('^vorbis/', 'vorbis'),
    ('^FLAC/', 'flac'),
    ('^opus/', 'opus'),
    ('^speex/speex_resampler\\.h$', 'speexdsp'),
    ('^speex/', 'speex'),
    ('^dav1d/', 'dav1d'),
    ('^vpx/', 'vpx'),
    ('^aom/', 'aom'),
    ('^libbluray/', 'bluray'),
    ('^dvdnav/', 'dvdnav'),
    ('^dvdread/', 'dvdread'),
    ('^dvdcss/', 'dvdcss'),
    ('^mpg123\\.h$', 'mpg123'),
    ('^librist/', 'librist'),
    ('^srt/', 'srt'),
    ('^libssh2', 'ssh2'),
    ('^lua\\.h$|^lauxlib\\.h$|^lualib\\.h$', 'lua'),
    ('^taglib/', 'taglib'),
    ('^upnp/', 'upnp'),
    ('^ebml/', 'ebml'),
    ('^matroska/', 'matroska'),
    ('^google/protobuf/', 'protobuf'),
    ('^a52dec/', 'a52'),
    ('^dca\\.h$', 'dca'),
    ('^faad\\.h$|^neaacdec\\.h$', 'faad2'),
    ('^mad\\.h$', 'mad'),
    ('^mpeg2dec/', 'libmpeg2'),
    ('^theora/', 'theora'),
    ('^libxml/', 'libxml2'),
    ('^twolame\\.h$', 'twolame'),
    ('^x264\\.h$', 'x264'),
    ('^x265\\.h$', 'x265'),
    ('^libzvbi\\.h$', 'zvbi'),
    ('^chromaprint\\.h$', 'chromaprint'),
    ('^shout/', 'shout'),
    ('^libmodplug/', 'modplug'),
    ('^gme/', 'gme'),
    ('^fluidsynth\\.h$', 'fluid'),
    ('^spatialaudio/', 'spatialaudio'),
    ('^libnfs', 'nfs'),
    ('^nettle/', 'nettle'),
    ('^gmp\\.h$', 'gmp'),
    ('^fluidlite\\.h$', 'fluidlite'),
]


def logical_lines(text):
    """Join Make continuation lines without evaluating Make expressions."""
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        value = lines[index]
        index += 1
        while value.rstrip().endswith('\\') and index < len(lines):
            value = value.rstrip()[:-1] + ' ' + lines[index]
            index += 1
        yield value


def read_assignments(root):
    assignments = collections.defaultdict(list)
    for path in sorted((root / 'modules').rglob('Makefile.am')):
        for line in logical_lines(path.read_text()):
            match = re.match(r'^([A-Za-z0-9_]+)\s*(?:\+?=|:=|\?=)\s*(.*)', line)
            if match:
                assignments[match[1]].append(match[2].split(' #')[0])
    return assignments


def read_recipe_dependencies(recipes):
    dependencies = collections.defaultdict(set)
    for path in recipes.values():
        for line in logical_lines(path.read_text()):
            match = re.match(r'^DEPS_([A-Za-z0-9_-]+)\s*(?:\+?=|:=|\?=)\s*(.*)', line)
            if not match:
                continue
            value = re.sub(r'\$\([^)]*\)', ' ', match[2])
            tokens = set(re.findall(r'[A-Za-z0-9_.+-]+', value))
            tokens.update(re.findall(r'\$\(DEPS_([^)]*)\)', match[2]))
            dependencies[match[1]].update(token for token in tokens if token in recipes)
    return dependencies


def component_for_variable(variable, recipes):
    if variable in VARIABLE_ALIASES:
        return VARIABLE_ALIASES[variable]
    name = variable.removesuffix('_LIBS').removeprefix('LIBS_')
    if name in VARIABLE_ALIASES:
        return VARIABLE_ALIASES[name]
    for component in recipes:
        if component.lower() == name.lower():
            return component
    return None


def variable_references(value):
    return [left or right for left, right in re.findall(r'\$\(([^)]+)\)|\$\{([^}]+)\}', value)]


def source_license_grant(path):
    """Recognize explicit GNU license grants, without inferring other licenses."""
    header = path.read_text(errors='replace')[:6000].split('#include', 1)[0]
    if 'GNU Lesser General Public License' in header or 'GNU Library General Public License' in header:
        family = 'LGPL'
    elif 'GNU General Public License' in header:
        family = 'GPL'
    else:
        return None
    match = re.search(
        r'(?:either )?version\s+(\d+(?:\.\d+)?)\s+of the License[^\n]*(?:\n[^\n]*){0,3}',
        header,
        re.IGNORECASE,
    )
    if not match:
        return None
    version = match[1]
    if version in ('2', '3'):
        version += '.0'
    suffix = '-or-later' if re.search(r'any later version', match[0], re.IGNORECASE) else '-only'
    return family + '-' + version + suffix


def dependency_closure(components, dependencies):
    result = set()
    pending = list(components)
    while pending:
        component = pending.pop()
        if component in result:
            continue
        result.add(component)
        pending.extend(dependencies[component] - result)
    return result


def map_module(module, root, assignments, recipes, dependencies):
    source_paths = set()
    components = set()
    visited = set()

    def visit(variable):
        if variable in visited:
            return
        visited.add(variable)
        for value in assignments.get(variable, []):
            if variable.endswith('_SOURCES'):
                paths = re.findall(
                    r'(?:[A-Za-z0-9_.+-]+/)*[A-Za-z0-9_.+-]+\.(?:c|h|cc|cpp|hpp|m|mm|S)\b',
                    value,
                )
                for relative in paths:
                    path = root / 'modules' / relative
                    if path.exists():
                        source_paths.add(path)
            elif variable.endswith(('_LIBADD', '_LDFLAGS')):
                for reference in variable_references(value):
                    component = component_for_variable(reference, recipes)
                    if component:
                        components.add(component)
                local_libraries = re.findall(
                    r'(?:[A-Za-z0-9_./-]+/)?(lib[A-Za-z0-9_.-]+)\.la', value
                )
                for library in local_libraries:
                    target = library.replace('-', '_') + '_la_'
                    for suffix in ('SOURCES', 'LIBADD', 'LDFLAGS'):
                        visit(target + suffix)
                for library in re.findall(r'-l([A-Za-z0-9_.+-]+)', value):
                    component = component_for_variable(library, recipes)
                    if component:
                        components.add(component)
            for reference in variable_references(value):
                if reference in assignments and reference not in ('AM_LIBADD', 'AM_LDFLAGS'):
                    visit(reference)

    for suffix in ('SOURCES', 'LIBADD', 'LDFLAGS'):
        visit(module + '_la_' + suffix)
    grants = set()
    for path in sorted(source_paths):
        text = path.read_text(errors='replace')
        includes = re.findall(r'^\s*#\s*include\s*[<"]([^>"\n]+)[>"]', text, re.MULTILINE)
        for include in includes:
            for pattern, component in HEADER_PATTERNS:
                if re.search(pattern, include):
                    components.add(component)
        grant = source_license_grant(path)
        if grant:
            grants.add(grant)
    return {
        'source_files': sorted(path.relative_to(root).as_posix() for path in source_paths),
        'explicit_source_license_grants': sorted(grants),
        'direct_component_candidates': sorted(components),
        'transitive_component_candidates': sorted(dependency_closure(components, dependencies)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('vlc_source_root', type=pathlib.Path, help='Extracted VLC source directory.')
    parser.add_argument(
        '--native-files', type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().with_name('native-files.tsv'),
        help='Native inventory TSV. Default: native-files.tsv beside this script.',
    )
    parser.add_argument(
        '--output', type=pathlib.Path,
        help='Output TSV. Default: standard output.',
    )
    args = parser.parse_args()
    root = args.vlc_source_root.resolve()
    if not (root / 'modules').is_dir() or not (root / 'contrib/src').is_dir():
        parser.error('The source directory must contain modules and contrib/src.')
    counts = collections.Counter()
    with args.native_files.open(newline='') as inventory:
        for row in csv.DictReader(inventory, delimiter='\t'):
            name = pathlib.PurePosixPath(row['path']).stem
            if name.endswith('_plugin'):
                counts[name] += 1
    assignments = read_assignments(root)
    recipes = {path.parent.name: path for path in (root / 'contrib/src').glob('*/rules.mak')}
    dependencies = read_recipe_dependencies(recipes)
    output = args.output.open('w', newline='') if args.output else sys.stdout
    try:
        writer = csv.writer(output, delimiter='\t', lineterminator='\n')
        writer.writerow([
            'module', 'native_file_count', 'source_files', 'explicit_source_license_grants',
            'direct_component_candidates', 'transitive_component_candidates',
        ])
        for module, count in sorted(counts.items()):
            evidence = map_module(module, root, assignments, recipes, dependencies)
            writer.writerow([module, count] + [' | '.join(values) for values in evidence.values()])
    finally:
        if args.output:
            output.close()


if __name__ == '__main__':
    main()
