package mosaic

import (
	"image"
	"image/jpeg"
	"image/png"
	"log"
	"os"
	"path/filepath"

	"golang.org/x/image/draw"
)

func openImageFile(imageFilePath string) image.Image {
	imageFile, err := os.Open(imageFilePath)
	if err != nil {
		log.Fatal(err)
	}

	defer imageFile.Close()

	imageObject, _, err := image.Decode(imageFile)
	if err != nil {
		log.Fatal(err)
	}
	return imageObject
}

func resize(imageObject image.Image, widthPixels int, heightPixels int) image.Image {
	resizedImageObject := image.NewRGBA(image.Rect(0, 0, widthPixels, heightPixels))
	draw.NearestNeighbor.Scale(resizedImageObject, resizedImageObject.Rect, imageObject, imageObject.Bounds(), draw.Over, nil)
	return resizedImageObject
}

func crop(imageObject image.Image, startX int, startY int, endX int, endY int) image.Image {
	copiedImageObject := copyRGBA(imageObject)

	croppedImageObject := copiedImageObject.SubImage(image.Rect(startX, startY, endX, endY))
	return croppedImageObject
}

func transformGrayScale(imageObject image.Image) image.Image {
	greyScaleImageObject := image.NewGray(imageObject.Bounds())
	draw.Draw(greyScaleImageObject, greyScaleImageObject.Bounds(), imageObject, imageObject.Bounds().Min, draw.Src)

	return greyScaleImageObject
}

func copyRGBA(imageObject image.Image) *image.RGBA {
	copiedImageObject := image.NewRGBA(imageObject.Bounds())
	draw.Draw(copiedImageObject, copiedImageObject.Bounds(), imageObject, imageObject.Bounds().Min, draw.Src)

	return copiedImageObject
}

func saveImageFile(imageObject image.Image, outputPath string, formatType string) {
	// Make directory if not exists
	if _, err := os.Stat(outputPath); os.IsNotExist(err) {
		os.MkdirAll(filepath.Dir(outputPath), os.ModePerm)
	}

	outputFile, err := os.Create(outputPath)

	if err != nil {
		log.Fatal(err)
	}

	defer outputFile.Close()

	if formatType == "PNG" {
		saveToPNG(imageObject, outputFile)
	} else if formatType == "JPG" {
		saveToJPG(imageObject, outputFile)
	} else {
		log.Fatalf("Unknown format type: %v", formatType)
	}
}

func saveToPNG(imageObject image.Image, outputFile *os.File) {
	png.Encode(outputFile, imageObject)
}

func saveToJPG(imageObject image.Image, outputFile *os.File) {
	jpeg.Encode(outputFile, imageObject, nil)
}
