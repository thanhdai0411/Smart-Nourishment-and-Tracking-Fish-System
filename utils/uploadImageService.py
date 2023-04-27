from constant import CLOUDINARY_NAME,CLOUDINARY_API_KEY,CLOUDINARY_API_SECRET
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="CLOUDINARY CLOUD NAME",
    api_key="CLOUDINARY API KEY",
    api_secret="CLOUDINARY API SECRET"
)

def upload():
    if request.method == "POST":
        image = request.files["image"]
        description = request.form.get("description")
        if image and description and image.filename.split(".")[-1].lower() in ALLOWED_EXTENSIONS:
            upload_result = cloudinary.uploader.upload(image)
            mongo.db.gallery.insert_one({
                "url": upload_result["secure_url"],
                "description": description.strip()
            })

            flash("Successfully uploaded image to gallery!", "success")
            return redirect(url_for("upload"))
        else:
            flash("An error occurred while uploading the image!", "danger")
            return redirect(url_for("upload"))
    return render_template("upload.html")