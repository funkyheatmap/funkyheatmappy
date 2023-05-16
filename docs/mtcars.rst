################
Demo with mtcars
################

Import packages::

    from funkyheatmappy import funkyheatmap
    import pandas as pd

Load data::

    mtcars = pd.read_csv("../test/data/mtcars.csv")
    mtcars = mtcars.rename(columns={"Unnamed: 0": "id"})
    mtcars["data"] = (
            mtcars["data"].sort_values(by="mpg", ascending=False).reset_index(drop=True)
        )
    
We can plot this data frame without any additional formatting, though it doesn't look very nice::

    funkyheatmap(mtcars)

By defining a few additional formatting parameters, we can get the plot to look much nicer.

***********
Column info
***********

::
    
    column_info = pd.DataFrame(
        {
            "id": mtcars.columns,
            "group": [
                pd.NA,
                "overall",
                "overall",
                "group1",
                "group1",
                "group1",
                "group1",
                "group2",
                "group2",
                "group2",
                "group2",
                "group2",
            ],
            "name": [
                "",
                "Miles / gallon",
                "Number of cylinders",
                "Displacement (cu.in.)",
                "Gross horsepower",
                "Rear axle ratio",
                "Weight (1000 lbs)",
                "1/4 mile time",
                "Engine",
                "Transmission",
                "# Forward gears",
                "# Carburetors",
            ],
            "geom": [
                "text",
                "bar",
                "bar",
                "funkyrect",
                "funkyrect",
                "funkyrect",
                "funkyrect",
                "circle",
                "circle",
                "circle",
                "circle",
                "circle",
            ],
            "options": [
                {"ha": 0, "width": 6},
                {"width": 4, "legend": False},
                {"width": 4, "legend": False},
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
                dict(),
            ],
            "palette": [
                np.nan,
                "palette1",
                "palette2",
                "palette1",
                "palette1",
                "palette1",
                "palette1",
                "palette2",
                "palette2",
                "palette2",
                "palette2",
                "palette2",
            ],
        }
    )
    column_info.index = column_info["id"]


Define column groups
::

    column_groups = pd.DataFrame(
        {
            "Category": ["Overall", "Group1", "Group2"],
            "group": ["overall", "group1", "group2"],
            "palette": ["overall", "palette1", "palette2"],
        }
    )


********
Row info
********

Determine method grouping::

    row_info = pd.DataFrame({"id": mtcars["id"], "group": "test"}, index=mtcars["id"])
    row_groups = pd.DataFrame({"Group": ["Test"], "group": ["test"]})
    

********
Palettes
********

Determine palettes::

    palettes = pd.DataFrame(
        {
            "palettes": ["overall", "palette1", "palette2"],
            "colours": [colors, "Blues", "Reds"],
        }
    )


************
Funkyheatmap
************

::
     
    funkyheatmap(
        data=mtcars,
        column_info=mtcarscolumn_info,
        column_groups=column_groups,
        row_info=row_info,
        row_groups=row_groups,
        palettes=palettes,
        expand={"xmax": 4},
    )


**********
Add images
**********

Add a new column to the mtcars data and to the column info::


    mtcars["data"]["type"] = np.concatenate(
        (np.repeat("ice", 10), np.repeat("electric", 22))
    )

    mtcars["column_info"] = pd.concat(
        [
            mtcars["column_info"],
            pd.DataFrame(
                {
                    "id": ["type"],
                    "group": ["group2"],
                    "name": ["Type of engine"],
                    "geom": ["image"],
                    "options": [{"path": "../test/data/", "filetype": "png"}],
                    "palette": [np.nan],
                },
                index=["type"],
            ),
        ]
    )

Generate funkyheatmap::

    funkyheatmap(
        data=mtcars,
        column_info=column_info,
        column_groups=column_groups,
        row_info=row_info,
        row_groups=row_groups,
        palettes=palettes,
        expand={"xmax": 4},
    )

Additionally you can add a zoom parameter to the options in column info which is used to shrink or expand the image::

    mtcars["column_info"] = pd.concat(
        [
            mtcars["column_info"],
            pd.DataFrame(
                {
                    "id": ["type"],
                    "group": ["group2"],
                    "name": ["Type of engine"],
                    "geom": ["image"],
                    "options": [{"path": "../test/data/", "filetype": "png", "zoom": 0.5"}],
                    "palette": [np.nan],
                },
                index=["type"],
            ),
        ]
    )

    funkyheatmap(
        data=mtcars,
        column_info=column_info,
        column_groups=column_groups,
        row_info=row_info,
        row_groups=row_groups,
        palettes=palettes,
        expand={"xmax": 4},
    )
