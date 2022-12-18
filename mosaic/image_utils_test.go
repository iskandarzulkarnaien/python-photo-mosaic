package mosaic

import (
	"fmt"
	"testing"

	"github.com/vitali-fedulov/images4"
)

const TEST_IMAGE_DIRECTORY = "test_images/"
const TEST_REFERENCE_DIRECTORY = TEST_IMAGE_DIRECTORY + "test_references/"
const TEST_OUTPUTS_DIRECTORY = TEST_IMAGE_DIRECTORY + "test_outputs/"

const ORIGINAL_IMAGE_PATH = TEST_IMAGE_DIRECTORY + "original.jpg"

func TestResize(t *testing.T) {
	originalImageObject := openImageFile(ORIGINAL_IMAGE_PATH)
	originalWidth := originalImageObject.Bounds().Dx()
	originalHeight := originalImageObject.Bounds().Dy()

	for _, scalingFactor := range [2]float32{8, 0.5} {
		targetResizedWidth := int(float32(originalWidth) * scalingFactor)
		targetResizedHeight := int(float32(originalHeight) * scalingFactor)

		resizedImageObject := resize(originalImageObject, targetResizedWidth, targetResizedHeight)
		resizedWidth := resizedImageObject.Bounds().Dx()
		resizedHeight := resizedImageObject.Bounds().Dy()

		if resizedWidth != targetResizedWidth {
			t.Errorf("Expected resizedWidth of %v but got %v instead (originalWidth: %v, scalingFactor: %v)",
				targetResizedWidth, resizedWidth, originalWidth, scalingFactor)
		}

		if resizedHeight != targetResizedHeight {
			t.Errorf("Expected resizedHeight of %v but got %v instead (originalHeight: %v, scalingFactor: %v)",
				targetResizedHeight, resizedHeight, originalHeight, scalingFactor)
		}

		originalIcon := images4.Icon(originalImageObject)
		resizedIcon := images4.Icon(resizedImageObject)

		if !images4.Similar(originalIcon, resizedIcon) {
			t.Errorf("Resizing by factor %v did not return similar images", scalingFactor)
		}

		saveImageFile(resizedImageObject, TEST_OUTPUTS_DIRECTORY+fmt.Sprintf("TestResize/Resized%f.jpg", scalingFactor), "JPG")
	}
	saveImageFile(originalImageObject, TEST_OUTPUTS_DIRECTORY+"TestResize/Original.jpg", "JPG")
}

func TestCrop(t *testing.T) {
	originalImageObject := openImageFile(ORIGINAL_IMAGE_PATH)
	originalMinX := originalImageObject.Bounds().Min.X
	originalMinY := originalImageObject.Bounds().Min.Y
	originalMaxX := originalImageObject.Bounds().Max.X
	originalMaxY := originalImageObject.Bounds().Max.Y

	topHalfCoords := [4]int{originalMinX, originalMinY, originalMaxX, originalMaxY / 2}
	leftHalfCoords := [4]int{originalMinX, originalMinY, originalMaxX / 2, originalMaxY}
	middlePortionCoords := [4]int{(originalMinX + originalMaxX) / 4, (originalMinY + originalMaxY) / 4, (originalMinX + originalMaxX) * 3 / 4, (originalMinY + originalMaxY) * 3 / 4}

	// centerPortionCoords := [4]int{}

	baseFileLocation := "TestCrop/"
	for _, coords := range [3][4]int{topHalfCoords, leftHalfCoords, middlePortionCoords} {
		startX, startY, endX, endY := coords[0], coords[1], coords[2], coords[3]

		croppedImageObject := crop(originalImageObject, startX, startY, endX, endY)

		croppedFileName := ""
		switch coords {
		case topHalfCoords:
			croppedFileName = "topHalf.jpg"
		case leftHalfCoords:
			croppedFileName = "leftHalf.jpg"
		case middlePortionCoords:
			croppedFileName = "middlePortion.jpg"
		default:
			t.Errorf("Case for coords %v not found, did you forget to implement?", coords)
		}
		croppedFileLocation := baseFileLocation + croppedFileName

		referenceImageObject := openImageFile(TEST_REFERENCE_DIRECTORY + croppedFileLocation)

		referenceImageIcon := images4.Icon(referenceImageObject)
		croppedImageIcon := images4.Icon(croppedImageObject)
		if !images4.Similar(referenceImageIcon, croppedImageIcon) {
			t.Errorf("Crop for %v did not return similar images", croppedFileName)
		}

		saveImageFile(croppedImageObject, TEST_OUTPUTS_DIRECTORY+croppedFileLocation, "JPG")
	}
	saveImageFile(originalImageObject, TEST_OUTPUTS_DIRECTORY+baseFileLocation+"/Original.jpg", "JPG")
}

func TestTransformGrayScale(t *testing.T) {

}
