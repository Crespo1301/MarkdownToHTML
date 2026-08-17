#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

ffmpeg -y -loglevel error \
  -i exports/carousel-1.png \
  -i exports/carousel-2.png \
  -i exports/carousel-3.png \
  -i exports/carousel-4.png \
  -i exports/carousel-5.png \
  -i exports/story-cover.png \
  -filter_complex \
  "[0:v]scale=280:350:force_original_aspect_ratio=decrease,pad=300:390:(ow-iw)/2:10:color=0xeef0ec,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='carousel-1.png':x=10:y=365:fontsize=14:fontcolor=0x17231d[a];
   [1:v]scale=280:350:force_original_aspect_ratio=decrease,pad=300:390:(ow-iw)/2:10:color=0xeef0ec,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='carousel-2.png':x=10:y=365:fontsize=14:fontcolor=0x17231d[b];
   [2:v]scale=280:350:force_original_aspect_ratio=decrease,pad=300:390:(ow-iw)/2:10:color=0xeef0ec,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='carousel-3.png':x=10:y=365:fontsize=14:fontcolor=0x17231d[c];
   [3:v]scale=280:350:force_original_aspect_ratio=decrease,pad=300:390:(ow-iw)/2:10:color=0xeef0ec,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='carousel-4.png':x=10:y=365:fontsize=14:fontcolor=0x17231d[d];
   [4:v]scale=280:350:force_original_aspect_ratio=decrease,pad=300:390:(ow-iw)/2:10:color=0xeef0ec,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='carousel-5.png':x=10:y=365:fontsize=14:fontcolor=0x17231d[e];
   [5:v]scale=280:350:force_original_aspect_ratio=decrease,pad=300:390:(ow-iw)/2:10:color=0xeef0ec,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='story-cover.png':x=10:y=365:fontsize=14:fontcolor=0x17231d[f];
   [a][b][c][d][e][f]xstack=inputs=6:layout=0_0|300_0|600_0|0_390|300_390|600_390:fill=0xeef0ec[out]" \
  -map "[out]" \
  -frames:v 1 \
  exports/contact-sheet.png

ffmpeg -y -loglevel error \
  -i exports/tiktok-1.png \
  -i exports/tiktok-2.png \
  -i exports/tiktok-3.png \
  -i exports/tiktok-4.png \
  -i exports/tiktok-5.png \
  -filter_complex \
  "[0:v]scale=180:320:force_original_aspect_ratio=decrease,pad=200:360:(ow-iw)/2:10:color=0xeef0ec,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='tiktok-1.png':x=10:y=335:fontsize=14:fontcolor=0x17231d[a];
   [1:v]scale=180:320:force_original_aspect_ratio=decrease,pad=200:360:(ow-iw)/2:10:color=0xeef0ec,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='tiktok-2.png':x=10:y=335:fontsize=14:fontcolor=0x17231d[b];
   [2:v]scale=180:320:force_original_aspect_ratio=decrease,pad=200:360:(ow-iw)/2:10:color=0xeef0ec,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='tiktok-3.png':x=10:y=335:fontsize=14:fontcolor=0x17231d[c];
   [3:v]scale=180:320:force_original_aspect_ratio=decrease,pad=200:360:(ow-iw)/2:10:color=0xeef0ec,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='tiktok-4.png':x=10:y=335:fontsize=14:fontcolor=0x17231d[d];
   [4:v]scale=180:320:force_original_aspect_ratio=decrease,pad=200:360:(ow-iw)/2:10:color=0xeef0ec,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='tiktok-5.png':x=10:y=335:fontsize=14:fontcolor=0x17231d[e];
   [a][b][c][d][e]xstack=inputs=5:layout=0_0|200_0|400_0|600_0|800_0:fill=0xeef0ec[out]" \
  -map "[out]" \
  -frames:v 1 \
  exports/tiktok-contact-sheet.png

ffmpeg -y -loglevel error \
  -i exports/tiktok-safe-check-1.png \
  -i exports/tiktok-safe-check-2.png \
  -i exports/tiktok-safe-check-3.png \
  -i exports/tiktok-safe-check-4.png \
  -i exports/tiktok-safe-check-5.png \
  -filter_complex \
  "[0:v]scale=180:320:force_original_aspect_ratio=decrease,pad=200:360:(ow-iw)/2:10:color=0xeef0ec,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='safe-check-1.png':x=10:y=335:fontsize=13:fontcolor=0x17231d[a];
   [1:v]scale=180:320:force_original_aspect_ratio=decrease,pad=200:360:(ow-iw)/2:10:color=0xeef0ec,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='safe-check-2.png':x=10:y=335:fontsize=13:fontcolor=0x17231d[b];
   [2:v]scale=180:320:force_original_aspect_ratio=decrease,pad=200:360:(ow-iw)/2:10:color=0xeef0ec,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='safe-check-3.png':x=10:y=335:fontsize=13:fontcolor=0x17231d[c];
   [3:v]scale=180:320:force_original_aspect_ratio=decrease,pad=200:360:(ow-iw)/2:10:color=0xeef0ec,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='safe-check-4.png':x=10:y=335:fontsize=13:fontcolor=0x17231d[d];
   [4:v]scale=180:320:force_original_aspect_ratio=decrease,pad=200:360:(ow-iw)/2:10:color=0xeef0ec,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='safe-check-5.png':x=10:y=335:fontsize=13:fontcolor=0x17231d[e];
   [a][b][c][d][e]xstack=inputs=5:layout=0_0|200_0|400_0|600_0|800_0:fill=0xeef0ec[out]" \
  -map "[out]" \
  -frames:v 1 \
  exports/tiktok-safe-zone-check.png
