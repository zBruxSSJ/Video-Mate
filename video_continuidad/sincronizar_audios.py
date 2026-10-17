#!/usr/bin/env python3
"""
sincronizar_audios.py
======================
Toma los 6 videos mudos de `renders/` y los audios reales grabados por el
equipo, y arma `Video_Final.mp4` con las voces sincronizadas.

Uso:
    python3 sincronizar_audios.py --audios /ruta/a/audios --out Video_Final.mp4

Carpeta de audios esperada (.mp3 / .m4a / .wav / .aac / .ogg), nombrados con
el número de escena en el nombre, por ejemplo:

    escena1.mp3   escena_2.m4a   Escena-3-evitable.wav  ...  escena5.mp3

La Escena 6 (cierre, hablan los 4 integrantes) puede grabarse de dos formas:
  a) Un solo archivo "escena6.mp3" (todos graban juntos, pasándose el turno).
  b) Varios clips cortos para la misma escena, por ejemplo:
         escena6_1.mp3  escena6_2.mp3  escena6_3.mp3  escena6_4.mp3
     En ese caso se concatenan automáticamente en orden alfabético/numérico
     antes de sincronizarlos con el video.
Esta misma lógica de "varios clips por escena" funciona para cualquier otra
escena si alguna vez necesitan dividirla en más de un archivo.

Si para alguna escena no se encuentra audio, esa escena se deja muda (con su
duración original) y se avisa por consola.

Lógica de sincronización por escena:
  - Si el audio dura MÁS que el video mudo: se extiende el video congelando
    su último cuadro el tiempo que haga falta.
  - Si el audio dura MENOS que el video mudo: se recorta el video a la
    duración del audio.
  - Si duran igual (tolerancia de 0.05 s): se mezclan directamente.

Al final, los 6 clips con audio se concatenan en `Video_Final.mp4`.
"""
import argparse
import re
import shlex
import subprocess
from pathlib import Path

AUDIO_EXTS = (".mp3", ".m4a", ".wav", ".aac", ".ogg", ".flac")
SCENE_FILES = [
    "scene1_intro.mp4",
    "scene2_concepto.mp4",
    "scene3_evitable.mp4",
    "scene4_salto.mp4",
    "scene5_infinita.mp4",
    "scene6_repaso.mp4",
]
SCENE_NAMES = [
    "Introducción", "Concepto de continuidad", "Discontinuidad evitable",
    "Discontinuidad de salto", "Discontinuidad infinita", "Repaso y conclusión",
]

HERE = Path(__file__).resolve().parent


def run(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("ERROR ejecutando:", " ".join(shlex.quote(c) for c in cmd))
        print(result.stderr)
        raise SystemExit(1)
    return result.stdout


def ffprobe_duration(path):
    out = run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(path),
    ])
    return float(out.strip())


def find_audio_files_for_scene(audio_dir, scene_num):
    """Devuelve la lista (ordenada) de archivos de audio que matchean una escena.
    Acepta tanto 'escenaN.ext' (un solo archivo) como 'escenaN_1.ext',
    'escenaN_2.ext', ... (varios clips para la misma escena)."""
    candidates = []
    for f in sorted(audio_dir.iterdir()):
        if f.suffix.lower() not in AUDIO_EXTS:
            continue
        stem = f.stem.lower().replace("escena", "").replace("scene", "")
        stem = stem.lstrip("-_ ")
        m = re.match(r"^(\d+)([_\-](\d+))?", stem)
        if not m:
            continue
        if int(m.group(1)) != scene_num:
            continue
        sub_idx = int(m.group(3)) if m.group(3) else 0
        candidates.append((sub_idx, f))
    candidates.sort(key=lambda t: t[0])
    return [f for _, f in candidates]


def concat_audio_clips(clips, out_path):
    if len(clips) == 1:
        return clips[0]
    inputs = []
    for c in clips:
        inputs += ["-i", str(c)]
    filter_inputs = "".join(f"[{i}:a]" for i in range(len(clips)))
    filt = f"{filter_inputs}concat=n={len(clips)}:v=0:a=1[a]"
    run(["ffmpeg", "-y", *inputs, "-filter_complex", filt, "-map", "[a]", str(out_path)])
    return out_path


def build_scene_clip(video_path, audio_path, out_path, fps=24):
    video_dur = ffprobe_duration(video_path)

    if audio_path is None:
        print(f"  [!] Sin audio para {video_path.name}; se mantiene silenciosa "
              f"({video_dur:.2f}s).")
        run([
            "ffmpeg", "-y", "-i", str(video_path),
            "-f", "lavfi", "-t", str(video_dur), "-i", "anullsrc=r=44100:cl=stereo",
            "-c:v", "copy", "-c:a", "aac", "-shortest", str(out_path),
        ])
        return video_dur

    audio_dur = ffprobe_duration(audio_path)
    diff = audio_dur - video_dur
    print(f"  video={video_dur:.2f}s  audio={audio_dur:.2f}s  diff={diff:+.2f}s")

    if abs(diff) <= 0.05:
        run([
            "ffmpeg", "-y", "-i", str(video_path), "-i", str(audio_path),
            "-map", "0:v:0", "-map", "1:a:0",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
            "-shortest", str(out_path),
        ])
    elif diff > 0:
        run([
            "ffmpeg", "-y", "-i", str(video_path), "-i", str(audio_path),
            "-filter_complex",
            f"[0:v]tpad=stop_mode=clone:stop_duration={diff:.3f}[v]",
            "-map", "[v]", "-map", "1:a:0",
            "-r", str(fps), "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-profile:v", "high", "-b:v", "9000k",
            "-c:a", "aac", "-b:a", "192k",
            str(out_path),
        ])
    else:
        run([
            "ffmpeg", "-y", "-i", str(video_path), "-i", str(audio_path),
            "-map", "0:v:0", "-map", "1:a:0",
            "-t", f"{audio_dur:.3f}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
            "-b:v", "9000k", "-r", str(fps),
            "-c:a", "aac", "-b:a", "192k",
            str(out_path),
        ])
    return max(video_dur, audio_dur)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--audios", required=True, help="Carpeta con los audios grabados.")
    ap.add_argument("--renders", default=str(HERE / "renders"),
                     help="Carpeta con los 6 MP4 mudos (default: ./renders).")
    ap.add_argument("--work", default=str(HERE / "renders" / "con_audio"),
                     help="Carpeta de trabajo para los clips intermedios con audio.")
    ap.add_argument("--out", default=str(HERE / "Video_Final.mp4"),
                     help="Archivo de salida final.")
    args = ap.parse_args()

    audio_dir = Path(args.audios)
    renders_dir = Path(args.renders)
    work_dir = Path(args.work)
    work_dir.mkdir(parents=True, exist_ok=True)

    if not audio_dir.is_dir():
        print(f"La carpeta de audios no existe: {audio_dir}")
        raise SystemExit(1)

    clip_paths = []
    total = 0.0
    for i, (video_name, scene_name) in enumerate(zip(SCENE_FILES, SCENE_NAMES), start=1):
        video_path = renders_dir / video_name
        if not video_path.exists():
            print(f"[ERROR] No se encontró {video_path}. Renderizá las escenas primero.")
            raise SystemExit(1)

        audio_files = find_audio_files_for_scene(audio_dir, i)
        if not audio_files:
            audio_path = None
            print(f"Escena {i} ({scene_name}): audio = — no encontrado —")
        elif len(audio_files) == 1:
            audio_path = audio_files[0]
            print(f"Escena {i} ({scene_name}): audio = {audio_path.name}")
        else:
            names = ", ".join(f.name for f in audio_files)
            print(f"Escena {i} ({scene_name}): {len(audio_files)} clips -> concatenando "
                  f"({names})")
            audio_path = concat_audio_clips(audio_files, work_dir / f"audio_escena{i}.wav")

        out_clip = work_dir / f"clip{i}.mp4"
        dur = build_scene_clip(video_path, audio_path, out_clip)
        total += dur
        clip_paths.append(out_clip)

    concat_list = work_dir / "concat_list.txt"
    with open(concat_list, "w") as f:
        for p in clip_paths:
            f.write(f"file '{p.resolve()}'\n")

    print(f"\nConcatenando {len(clip_paths)} clips (duración total ≈ {total:.1f}s)…")
    run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
        "-b:v", "9000k", "-r", "24", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", str(args.out),
    ])

    final_dur = ffprobe_duration(args.out)
    print(f"\n[OK] Video final exportado: {args.out}")
    print(f"     Duración total: {final_dur:.1f}s  ({final_dur/60:.2f} min)")


if __name__ == "__main__":
    main()
