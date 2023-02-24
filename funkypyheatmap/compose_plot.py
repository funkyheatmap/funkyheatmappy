import matplotlib.pyplot as plt
import numpy as np

from funkypyheatmap.add_column_if_missing import add_column_if_missing
from matplotlib import collections as mc
from matplotlib.patches import Rectangle, Circle


def compose_plot(positions, expand):
    fig, ax = plt.subplots()

    # Plot row backgrounds
    df = positions["row_pos"]
    df = df[df["color_background"]]

    if df.shape[0] > 0:
        for _, row in df.iterrows():
            rect = Rectangle(
                xy=(
                    np.min(positions["column_pos"]["xmin"]) - 0.25,
                    row["ymin"] - (positions["viz_params"] / 2),
                ),
                width=np.max(positions["column_pos"]["xmax"]) + 0.25,
                height=row["height"] + positions["viz_params"] / 2,
                color="#DDDDDD",
                zorder=0,
            )
            ax.add_patch(rect)

    # Plot segments
    if positions["segment_data"].shape[0] > 0:
        df = add_column_if_missing(
            positions["segment_data"], size=0.5, colour="black", linetype="solid"
        )
        lines = [
            [(row["x"], row["y"]), (row["xend"], row["yend"])]
            for _, row in df.iterrows()
        ]
        lc = mc.LineCollection(lines, linewidths=df["size"], colors=df["colour"])
        lc.set_linewidth(0.5)
        lc.set_zorder(0)
        ax.add_collection(lc)

    # Plot rectangles
    if positions["rect_data"].shape[0] > 0:
        df = add_column_if_missing(
            positions["rect_data"], border_colour="black", border=True, alpha=1
        )
        df.assign("border_colour", df["border_colour"] if df["border"] else np.nan)
        rect = Rectangle(
            xy=(df["xmin"], df["ymin"]),
            width=df["xmax"] - df["xmin"],
            height=df["ymax"] - df["ymin"],
        )

    # Plot circles
    if positions["circle_data"].shape[0] > 0:
        for _, row in positions["circle_data"].iterrows():
            circle = Circle(
                xy=(row["x0"], row["y0"]), radius=row["r"], color=row["colour"]
            )
            ax.add_patch(circle)

    # Plot funky rectangles
    if positions["funkyrect_data"].shape[0] > 0:
        pass

    # Plot pies
    if positions["pie_data"].shape[0] > 0:
        pass

    if positions["text_data"].shape[0] > 0:
        df = add_column_if_missing(
            positions["text_data"],
            hjust=0.5,
            vjust=0.5,
            size=4,
            fontface="plain",
            colour="black",
            lineheight=1,
            angle=0,
        )
        df = df.assign(angle2=np.multiply(np.divide(df["angle"], 360), 2 * np.pi))
        df = df.assign(
            cosa=np.round(np.cos(df["angle2"]), 2),
            sina=np.round(np.sin(df["angle2"]), 2),
        )
        df = df.assign(
            alphax=np.add(
                (
                    np.multiply(
                        (
                            [
                                1 - df["hjust"].iloc[i]
                                if c < 0
                                else df["hjust"].iloc[i]
                                for i, c in enumerate(df["cosa"])
                            ]
                        ),
                        np.abs(df["cosa"]),
                    )
                ),
                (
                    np.multiply(
                        (
                            [
                                np.subtract(1, df["vjust"].iloc[i])
                                if s > 0
                                else df["vjust"].iloc[i]
                                for i, s in enumerate(df["sina"])
                            ]
                        ),
                        np.abs(df["sina"]),
                    )
                ),
            ),
            alphay=np.add(
                (
                    np.multiply(
                        (
                            [
                                np.subtract(1, df["hjust"].iloc[i])
                                if s < 0
                                else df["hjust"].iloc[i]
                                for i, s in enumerate(df["sina"])
                            ]
                        ),
                        np.abs(df["sina"]),
                    )
                ),
                (
                    np.multiply(
                        (
                            [
                                np.subtract(1, df["vjust"].iloc[i])
                                if c < 0
                                else df["vjust"].iloc[i]
                                for i, c in enumerate(df["cosa"])
                            ]
                        ),
                        np.abs(df["cosa"]),
                    )
                ),
            ),
        )
        df = df.assign(
            x=np.add(
                np.multiply((np.subtract(1, df["alphax"])), df["xmin"]),
                np.multiply(df["alphax"], df["xmax"]),
            ),
            y=np.add(
                np.multiply((np.subtract(1, df["alphay"])), df["ymin"]),
                np.multiply(df["alphay"], df["ymax"]),
            ),
        )

        df = df[df["label_value"] != ""]
        for _, row in df.iterrows():
            ax.text(
                x=row["x"],
                y=row["y"],
                s=row["label_value"],
                size=row["size"],
                color=row["colour"],
                rotation=row["angle"],
                ha="center",
                va="center",
            )

    ax.axis("equal")
    plt.axis("off")
    plt.show()
    print("hello")
