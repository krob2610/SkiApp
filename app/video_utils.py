import datetime
import os

import ffmpy
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation

from app.labels_namespace import ORIENTATION, OTHER


def select_data_range(start: str, end: str, df: pd.DataFrame):
    """Select a range of data from a DataFrame based on the start and end times."""
    start_time = pd.to_datetime(start).time()
    end_time = pd.to_datetime(end).time()

    # throw an exception when the start time is greater than the end time
    if start_time > end_time:
        raise ValueError("The start time cannot be greater than the end time.")

    # Select data between start_time and end_time
    return df.between_time(start_time, end_time)


def gif_to_mp4(input: str, output: str) -> None:
    """Convert a GIF file to an MP4 file."""
    ff = ffmpy.FFmpeg(inputs={input: None}, outputs={output: None})
    ff.run()


def draw_plot_plt(
    df: pd.DataFrame,
    start: str,
    end: str,
    col: str,
    output: str,
    window_size: int = 100,
):
    """Function to create a plot for each value in a given column over time."""
    df_copy = df.copy()
    df_copy = select_data_range(df=df_copy, start=start, end=end)
    if "time" not in df_copy.columns:
        df_copy.reset_index(inplace=True)
    df_split = df_copy[col].apply(pd.Series)

    labels = ORIENTATION if col == "Orientation" else OTHER

    fig, ax = plt.subplots(figsize=(10, 6))

    # Set the y-axis limits
    ax.set_ylim(df_split.min().min(), df_split.max().max())

    def update(frame):
        ax.clear()
        for i, (cord, label) in enumerate(zip(df_split.columns, labels)):
            if col == "Orientation" and i < 4:
                continue
            ax.plot(
                df_copy["time"].iloc[: frame + 1],
                df_split[cord].iloc[: frame + 1],
                label=f"{label}",
            )
        ax.set_title(f"{col} over time")
        ax.set_xlabel("time")
        ax.set_ylabel(col)
        ax.legend()

        # Keep the y-axis limits fixed
        ax.set_ylim(df_split.min().min(), df_split.max().max())

        # Set the x-axis limits to create a moving window of window_size seconds
        if frame > window_size:
            ax.set_xlim(
                df_copy["time"].iloc[frame - window_size], df_copy["time"].iloc[frame]
            )

    duration = (df_copy["time"].iloc[-1] - df_copy["time"].iloc[0]).total_seconds()

    frames = len(df_copy)

    # Calculate the duration of one frame of the animation
    if frames > 1:
        frame_duration = (
            df_copy["time"].iloc[1] - df_copy["time"].iloc[0]
        ).total_seconds()
    else:
        frame_duration = duration

    # Prepare the animation
    ani = FuncAnimation(
        fig, update, frames=frames, repeat=False, interval=frame_duration * 1000
    )

    # Save the animation to a GIF file
    file_name = f"{output}.gif"

    ani.save(file_name, writer="pillow", fps=1 / frame_duration)

    plt.close()
    gif_to_mp4(input=file_name, output=file_name.replace(".gif", ".mp4"))
    print(
        f"Animation saved as {file_name}. Please open the file to view the animation."
    )


def cut_video(input_path: str, output_path: str, start: str, end: str):
    ff = ffmpy.FFmpeg(
        inputs={input_path: None}, outputs={output_path: f"-ss {start} -to {end}"}
    )
    ff.run()


def merge_videos(input1: str, input2: str, output: str):
    ff = ffmpy.FFmpeg(
        inputs={input1: None, input2: None},
        outputs={output: '-filter_complex "[0:v][1:v]vstack=inputs=2[v]" -map "[v]"'},
    )
    ff.run()
