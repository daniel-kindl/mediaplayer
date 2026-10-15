# Upstream build record request


This request is prepared for the [VideoLAN VLC issue tracker](https://code.videolan.org/videolan/vlc/-/issues). It has not been posted.

Title: Build input records for official VLC 3.0.24 Windows and macOS releases

We are auditing the native files shipped in VideoLAN.LibVLC.Windows 3.0.24 and VideoLAN.LibVLC.Mac 3.1.3.2. We compared all 1,574 native files against the corresponding official VLC 3.0.24 release archives; all native payload hashes match. All five libvlccore binaries identify revision 3.0.24-rc1-0-g6de05adcba.

We found the Windows release build logs in pipeline 741289, jobs 2841096, 2841097, 2841098. These give actual source archive hashes and configuration. The original job artifacts now return 404, and their logged *-release.7z hashes do not identify the later published plain .7z containers.

For macOS, pipeline 741287 jobs 2841088 and 2841089 build the same source commit. Their runner paths differ from the official release binaries, which contain /Users/videolan/vlc-3.0 build paths and Darwin 19 host settings. We have not treated those CI dependency receipts as exact release receipts.

Are the following records available for the official VLC 3.0.24 releases?

1. macOS Intel and ARM64 release build logs or dependency manifests: selected contrib source versions/hashes, applied patches, build settings, and any prebuilt contrib archive identity.
2. Windows release job output file hashes or retained release artifacts that connect jobs 2841096/2841097/2841098 to the published native files after signing/repackaging.
3. Any existing source bundle, license manifest, or retained release record that already contains this information.

A link to existing records is sufficient. We are keeping unproven dependency relationships explicitly open in the audit.
