#!/usr/bin/env python3
"""
sincronizar_audios.py
======================
Toma los 8 videos mudos de `renders/` y los audios reales grabados por cada
integrante del equipo, y arma `Video_Final.mp4` con las voces sincronizadas.

Uso:
    python3 sincronizar_audios.py --audios /ruta/a/audios --out Video_Final.mp4

Carpeta de audios esperada (un archivo por escena, cualquier extensión entre
.mp3 / .m4a / .wav / .aac / .ogg), nombrados con el número de escena en
cualquier parte del nombre, por ejemplo:

    escena1.mp3   escena_2.m4a   Escena-3-Fabrizio.wav   ... escena8.mp3

Si para alguna escena no se encuentra audio, esa escena se deja muda (con su
duración original) y se avisa por consola, para poder iterar sin tener que
grabar las 8 partes de una sola vez.

Lógica de sincronización por escena:
  - Si el audio dura MÁS que el video mudo: se extiende el video congelando
    su último cuadro el tiempo que haga falta (así no se corta la animación).
  - Si el audio dura MENOS que el video mudo: se recorta el video a la
    duración del audio.
  - Si duran igual (tolerancia de 0.05 s): se mezclan directamente.

Al final, los 8 clips con audio se concatenan (demuxer concat de ffmpeg) en
`Video_Final.mp4`.
"""
import argparse
import re
import shlex
import subprocess
import sys
from pathlib import Path

AUDIO_EXTS = (".mp3", ".m4a", ".wav", ".aac", ".ogg", ".flac")
SCENE_FILES = [
    "scene1_intro.mp4",
    "scene2_condiciones.mp4",
    "scene3_planteo.mp4",
    "scene4_condicion_x1.mp4",
    "scene5_condicion_x3.mp4",
    "scene6_resolver_sistema.mp4",
    "scene7_verificacion.mp4",
    "scene8_cierre.mp4",
]
SCENE_NAMES = [
    "Intro", "Condiciones de continuidad", "Planteo del problema",
    "Condición en x = 1", "Condición en x = 3", "Resolver el sistema",
    "Verificación gráfica", "Cierre",
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


def find_audio_for_scene(audio_dir, scene_num):
    pattern = re.compile(rf"(?<!\d){scene_num}(?!\d)")
    candidates = []
    for f in sorted(audio_dir.iterdir()):
        if f.suffix.lower() not in AUDIO_EXTS:
            continue
        stem = f.stem.lower().replace("escena", "").replace("scene", "")
        nums = re.findall(r"\d+", stem)
        if nums and nums[0] == str(scene_num):
            candidates.append(f)
    return candidates[0] if candidates else None


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
        # Audio más largo: congelamos el último cuadro del video para estirarlo.
        run([
            "ffmpeg", "-y", "-i", str(video_path), "-i", str(audio_path),
            "-filter_complex",
            f"[0:v]tpad=stop_mode=clone:stop_duration={diff:.3f}[v]",
            "-map", "[v]", "-map", "1:a:0",
            "-r", str(fps), "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-profile:v", "high", "-b:v", "6000k",
            "-c:a", "aac", "-b:a", "192k",
            str(out_path),
        ])
    else:
        # Audio más corto: recortamos el video a la duración del audio.
        run([
            "ffmpeg", "-y", "-i", str(video_path), "-i", str(audio_path),
            "-map", "0:v:0", "-map", "1:a:0",
            "-t", f"{audio_dur:.3f}",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
            "-b:v", "6000k", "-r", str(fps),
            "-c:a", "aac", "-b:a", "192k",
            str(out_path),
        ])
    return max(video_dur, audio_dur)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--audios", required=True, help="Carpeta con los audios grabados "
                                                      "(uno por escena).")
    ap.add_argument("--renders", default=str(HERE / "renders"),
                     help="Carpeta con los 8 MP4 mudos (default: ./renders).")
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

        audio_path = find_audio_for_scene(audio_dir, i)
        print(f"Escena {i} ({scene_name}): "
              f"audio = {audio_path.name if audio_path else '— no encontrado —'}")

        out_clip = work_dir / f"clip{i}.mp4"
        dur = build_scene_clip(video_path, audio_path, out_clip)
        total += dur
        clip_paths.append(out_clip)

    # Concatenar todos los clips con audio
    concat_list = work_dir / "concat_list.txt"
    with open(concat_list, "w") as f:
        for p in clip_paths:
            f.write(f"file '{p.resolve()}'\n")

    print(f"\nConcatenando {len(clip_paths)} clips (duración total ≈ {total:.1f}s)…")
    run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high",
        "-b:v", "6000k", "-r", "24", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", str(args.out),
    ])

    final_dur = ffprobe_duration(args.out)
    print(f"\n[OK] Video final exportado: {args.out}")
    print(f"     Duración total: {final_dur:.1f}s  ({final_dur/60:.2f} min)")


if __name__ == "__main__":
    main()
