# Phone-safe video delivery

Use this when a rendered `.mp4` fails on a phone, Telegram, WhatsApp, or another mobile player even though desktop playback works.

## Symptom pattern
- File has an `.mp4` extension
- Desktop players open it
- Mobile says *unsupported format* or refuses inline playback

## Common cause
The container is fine, but the video stream is encoded in a profile/pixel format many phones reject, especially:
- H.264 **High 4:4:4 Predictive**
- pixel format **`yuv444p`**

Mobile-safe delivery copies should usually be:
- video codec: **H.264**
- profile: **High** or Main
- pixel format: **`yuv420p`**
- audio: **AAC**
- MP4 moov atom moved to front with **`+faststart`**

## Verify before sending
```bash
ffprobe -v error \
  -show_entries format=filename,duration,size:stream=index,codec_name,codec_type,profile,pix_fmt,width,height,sample_rate,channels \
  -of json input.mp4
```

Red flags in the output:
- `profile: "High 4:4:4 Predictive"`
- `pix_fmt: "yuv444p"`

## Known-good re-encode
```bash
ffmpeg -y -i input.mp4 \
  -c:v libx264 \
  -pix_fmt yuv420p \
  -profile:v high \
  -level 4.1 \
  -movflags +faststart \
  -preset medium \
  -crf 20 \
  -c:a aac \
  -b:a 192k \
  output_phone.mp4
```

## Post-conversion verification
Run `ffprobe` again and confirm:
- H.264 profile is no longer 4:4:4
- `pix_fmt` is `yuv420p`
- audio is AAC

## Workflow note
Keep the original higher-fidelity master if you need it for archival or further editing. Send the phone-safe delivery copy to the user/platform.
