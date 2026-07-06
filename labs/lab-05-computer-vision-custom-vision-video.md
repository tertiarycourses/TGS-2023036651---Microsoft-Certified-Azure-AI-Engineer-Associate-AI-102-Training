# Lab 05 - Computer Vision, Custom Vision, Video Insights

## Objectives

- Analyze images with Azure AI Vision concepts.
- Select visual features for image processing requirements.
- Compare image classification and object detection.
- Plan custom vision training.
- Explain video insight scenarios.

## Scenario

The company wants to inspect product photos, detect damaged items, read text from images, and extract insights from product demo videos.

## Steps

### 1. Map Vision Requirements

| Requirement | Vision Capability |
| --- | --- |
| Generate image tags | Image analysis |
| Detect product locations | Object detection |
| Read text from photos | OCR |
| Classify product condition | Image classification |
| Extract video topics | Video insights |

### 2. Plan an Image Request

Document:

```text
Image source
Visual features
Language
Expected response fields
Error handling
Privacy considerations
```

### 3. Custom Vision Plan

Choose:

| Need | Model Type |
| --- | --- |
| One label for each image | Image classification |
| Locate multiple objects | Object detection |

Document image labels, training images, evaluation metrics, publishing, and consumption.

### 4. Video Insights Plan

Explain how Video Indexer can extract:

- Transcript.
- Keywords.
- Faces or speakers where appropriate.
- Topics.
- Scenes.

### 5. Responsible AI Review

Document consent, retention, face analysis sensitivity, and human review needs.

## Validation

You should have vision mapping, request plan, custom vision plan, video insight notes, and responsible AI review.

## Checkpoint Questions

1. What is OCR?
2. How is object detection different from classification?
3. What does a custom vision model require?
4. Why is video analysis sensitive?

## Course Focus

Vision solutions require selecting visual features, model type, evaluation approach, and responsible data handling.
