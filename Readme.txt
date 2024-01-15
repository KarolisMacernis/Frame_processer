An app with a GUI interface to change the naming and resolution of images in batch.

The purpose of the app is to change the naming and resolution of image files in the selected directory. Once the user
chooses the image directory it enables the options for choosing the new dpi setting for the images (dots per inch),
the new numbering convention and the project name. An "Adjusted Images" folder is created in the original path with
the new processed files.

Example:

If the user enters "Interior_walkthrough_animation" as the project name and chooses "_01, _02, ..." as the numbering
convention the processed images will be saved to the "Adjusted Images" folder as "Interior_walkthrough_animation_0001",
"Interior_walkthrough_animation_0002" and so on. The amount of zeros in front of the index will depend on the total
number of images being processed unless the user chooses a numbering convention without them. The resolution of the
images will also be changed according to the selected dpi option by the user.