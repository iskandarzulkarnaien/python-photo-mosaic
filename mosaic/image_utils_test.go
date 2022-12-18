package mosaic

import (
	"fmt"
	"testing"

	"github.com/vitali-fedulov/images4"
)

const TEST_IMAGE_DIRECTORY = "test_images/"
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

		save(originalImageObject, TEST_OUTPUTS_DIRECTORY+"TestResize/Original.jpg", "JPG")
		save(resizedImageObject, TEST_OUTPUTS_DIRECTORY+fmt.Sprintf("TestResize/Resized%f.jpg", scalingFactor), "JPG")
	}

}
