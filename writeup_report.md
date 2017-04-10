# Behaviorial Cloning


---

**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)


[image2]: ./examples/center.jpg "Center"
[image3]: ./examples/center_pic.jpg "Center 1 Image"
[image4]: ./examples/left_pic.jpg "Left1 Image"
[image5]: ./examples/right_pic.jpg "Right1 Image"
[image6]: ./examples/flip_1.jpg "flip1 Image"
[image7]: ./examples/flip_2.jpg "flip2 Image"
[image8]: ./examples/distribution.png "distribution"
[image9]: ./examples/NVIDIA.png "NVIDIA"

## Rubric Points
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.  

---
### Files Submitted & Code Quality

#### 1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* model.h5 containing a trained convolution neural network
* writeup_report.md or writeup_report.pdf summarizing the results

#### 2. Submission includes functional code
Using the Udacity provided simulator and my drive.py file, the car can be driven autonomously around the track by executing
```
python drive.py model.json
```
I modified the drive class so video could be produced

```
python drive.py model.json run1
```
```
python video.py run1
```

#### 3. Submission code is usable and readable

The model.py file contains the code for training and saving the convolution neural network. The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works.

### Model Architecture and Training Strategy

#### 1. An appropriate model architecture has been employed

My model consists of a convolution neural network with 2x2 filter sizes and depths between 24 and 48 (model.py lines 225-233)


#### 2. Attempts to reduce overfitting in the model

The model contains dropout layers in order to reduce overfitting (model.py lines starting from 227).

The model was trained and validated on different data sets to ensure that the model was not overfitting (Udacity's data and my own data seperatedly). The model was tested by running it through the simulator and ensuring that the vehicle could stay on the track.

#### 3. Model parameter tuning

The model used an adam optimizer, so the learning rate was not tuned manually (model.py line 255).

#### 4. Appropriate training data

Training data was chosen to keep the vehicle driving on the road. I used a combination of center lane driving, recovering from the left and right sides of the road and also used a gaming mouse instead of keyboard for steering.

For details about how I created the training data, see the next section.

### Model Architecture and Training Strategy

#### 1. Solution Design Approach


The overall strategy for deriving a model architecture was to use CNN to train the collected data set.

My first step was to use a convolution neural network model similar to the NVIDIA Architecture I thought this model might be appropriate because NVIDIA team used this model to train real car.


In order to gauge how well the model was working, I split my image and steering angle data into a training and validation set. I found that my first model had a low mean squared error on the training set but a high mean squared error on the validation set. This implied that the model was overfitting.

To combat the overfitting, I modified the model by implementing the dropout layer so that overfitting can be reduced.


The final step was to run the simulator to see how well the car was driving around track one. There were a few spots where the vehicle fell off the track, especially after the car run through the bridge. To improve the driving behavior in these cases, I recorded several extra drivings around there.

At the end of the process, the vehicle is able to drive autonomously around the track without leaving the road.

#### 2. Final Model Architecture

The final model architecture (model.py lines 50-68) consisted of a convolution neural network with the following layers and layer sizes
* Convolutional Layer 1: 5x5 with 24 depth and 2x2 max pooling
* Convolutional Layer 2: 5x5 with 36 depth and 2x2 max pooling
* Convolutional Layer 3: 5x5 with 48 depth and 2x2 max pooling
* Convolutional Layer 4: 3x3 with 64 depth
* Convolutional Layer 5: 3x3 with 64 depth
* Dropout Layers after ELU

![alt text][image9]


#### 3. Creation of the Training Set & Training Process
Here is an visualized distribution of steering angle from overall data
![alt text][image8]

To capture good driving behavior, I first recorded two laps on track one using center lane driving. Here is an example image of center lane driving:

![alt text][image2]

I then recorded the vehicle recovering from the left side and right sides of the road back to center so that the vehicle would learn to adjust angle when run off the track. These images show what a recovery looks like starting from side to center:

![alt text][image5]
![alt text][image4]
![alt text][image3]

Then I repeated this process on track two in order to get more data points.

To augment the data sat, I also flipped images and angles thinking that this would double the data size  For example, here is an image that has then been flipped:

![alt text][image6]
![alt text][image7]


After the collection process, I had 64k number of data points. I then preprocessed this data by running the model that I just created.


I finally randomly shuffled the data set and put 20% of the data into a validation set.

I used this training data for training the model. The validation set helped determine if the model was over or under fitting. The ideal number of epochs was 6 as evidenced by loss increasing. I used an adam optimizer so that manually training the learning rate wasn't necessary.
