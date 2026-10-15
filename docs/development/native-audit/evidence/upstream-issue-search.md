# Official issue and discussion search

Searched on 2026-10-15 UTC. Read-only investigation. No external issue, comment, or message was posted.

## Results

No retrieved issue or discussion supplied the missing exact macOS 3.0.24 release dependency receipts or a retained original Windows release artifact manifest. This is a result of the listed public searches, not a claim that such records do not exist.

- [VLC issue 26153: LGPL-only LibVLC CI builds for all platforms](https://code.videolan.org/videolan/vlc/-/issues/26153) discusses release ownership, build variants, and source-based license review. It has no matching dependency manifest or release log link. The [discussion endpoint](https://code.videolan.org/videolan/vlc/-/issues/26153/discussions.json) was accessible. API note and discussion endpoints returned 401.
- [VLC issue 30166: Reduce binary size](https://code.videolan.org/videolan/vlc/-/issues/30166) records 3.0.24 package size changes. It identifies static librist as a likely cause and discusses linker options. It supplies no matching release source manifest.
- [VLC issue 30115: 3.0.24 release test checklist](https://code.videolan.org/videolan/vlc/-/issues/30115) concerns platform and playback tests. Its discussion contains no release build receipt.
- [VLC issue 19095: SPDX compliance](https://code.videolan.org/videolan/vlc/-/issues/19095) requests SPDX support. The retrieved discussion contains no release SPDX manifest.
- [VLC issue 18851: aribb24 has incorrect license](https://code.videolan.org/videolan/vlc/-/issues/18851) is historical license ambiguity evidence. It cannot determine the license of the currently pinned aribb24 source. The current source review must make that determination.

## Query record

The broad GitLab search searches title and description. Multiword search can return issues whose build logs merely contain the terms. The macOS-release broad search reached its 100-item page limit, so its result is not exhaustive. The targeted title searches below reduce that noise.

- [videolan/vlc: `3.0.24`](https://code.videolan.org/api/v4/projects/videolan%2Fvlc/issues?scope=all&per_page=100&search=3.0.24): 50 results on the retrieved page.
- [videolan/vlc: `contrib manifest`](https://code.videolan.org/api/v4/projects/videolan%2Fvlc/issues?scope=all&per_page=100&search=contrib%20manifest): 4 results on the retrieved page.
- [videolan/vlc: `corresponding source`](https://code.videolan.org/api/v4/projects/videolan%2Fvlc/issues?scope=all&per_page=100&search=corresponding%20source): 24 results on the retrieved page.
- [videolan/vlc: `LGPL`](https://code.videolan.org/api/v4/projects/videolan%2Fvlc/issues?scope=all&per_page=100&search=LGPL): 8 results on the retrieved page.
- [videolan/vlc: `macOS release`](https://code.videolan.org/api/v4/projects/videolan%2Fvlc/issues?scope=all&per_page=100&search=macOS%20release): 100 results on the retrieved page.
- [videolan/libvlc-nuget: `3.0.24`](https://code.videolan.org/api/v4/projects/videolan%2Flibvlc-nuget/issues?scope=all&per_page=100&search=3.0.24): 0 results on the retrieved page.
- [videolan/libvlc-nuget: `contrib manifest`](https://code.videolan.org/api/v4/projects/videolan%2Flibvlc-nuget/issues?scope=all&per_page=100&search=contrib%20manifest): 0 results on the retrieved page.
- [videolan/libvlc-nuget: `corresponding source`](https://code.videolan.org/api/v4/projects/videolan%2Flibvlc-nuget/issues?scope=all&per_page=100&search=corresponding%20source): 0 results on the retrieved page.
- [videolan/libvlc-nuget: `LGPL`](https://code.videolan.org/api/v4/projects/videolan%2Flibvlc-nuget/issues?scope=all&per_page=100&search=LGPL): 0 results on the retrieved page.
- [videolan/libvlc-nuget: `macOS release`](https://code.videolan.org/api/v4/projects/videolan%2Flibvlc-nuget/issues?scope=all&per_page=100&search=macOS%20release): 0 results on the retrieved page.

Targeted searches use `in=title`:

- [`SBOM`](https://code.videolan.org/api/v4/projects/435/issues?scope=all&per_page=100&in=title&search=SBOM): 0 results.
- [`SPDX`](https://code.videolan.org/api/v4/projects/435/issues?scope=all&per_page=100&in=title&search=SPDX): 1 results.
- [`license manifest`](https://code.videolan.org/api/v4/projects/435/issues?scope=all&per_page=100&in=title&search=license%20manifest): 0 results.
- [`release build`](https://code.videolan.org/api/v4/projects/435/issues?scope=all&per_page=100&in=title&search=release%20build): 4 results.
- [`contrib sources`](https://code.videolan.org/api/v4/projects/435/issues?scope=all&per_page=100&in=title&search=contrib%20sources): 2 results.
- [`macOS build`](https://code.videolan.org/api/v4/projects/435/issues?scope=all&per_page=100&in=title&search=macOS%20build): 21 results.

The five libvlc-nuget project queries each returned an empty list. Raw results and issue descriptions are retained locally as public-issue-search.json and public-issue-search-targeted.json. Public discussion JSON for the relevant issues is also retained locally.

