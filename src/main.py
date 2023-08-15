import Beatmap.BeatmapFileImport
import Viewer.Render
import moviepy.editor as mpe

beatmap = Beatmap.BeatmapFileImport.import_beatmap("factal - Flux (Sharu) [liquid].osu")

Viewer.Render.render(beatmap)

clip = mpe.VideoFileClip("output.mp4")
audio = mpe.AudioFileClip("audio.mp3")
clip = clip.set_audio(audio)
clip.write_videofile("flux.mp4",fps=60)