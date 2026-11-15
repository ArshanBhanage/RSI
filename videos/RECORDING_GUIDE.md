# Recording guide

The owner deferred the 20 required walkthroughs. Nothing in the current manifest claims a finished video or YouTube URL.

For each entry, run its `recording_script` from the repository root while capturing the terminal and editor. The script shows the actual source and re-verifies persisted real evidence; it does not replay invented console output. Follow the planned narration file, replacing its status only after recording your own voice. Show the command, evaluator ID, failures, measured values and fidelity caveat on screen.

Render H.264/yuv420p MP4 at 1080p. Verify with:

```sh
ffprobe -v error -show_format -show_streams videos/renders/VIDEO.mp4
ffmpeg -v error -i videos/renders/VIDEO.mp4 -f null -
shasum -a 256 videos/renders/VIDEO.mp4
```

Update duration/checksum/status only from these commands. Upload to YouTube as unlisted or public as permitted, then verify each URL in a logged-out browser before setting `youtube_verified: true`.
