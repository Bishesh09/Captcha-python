import io
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Function to generate CAPTCHA image
def generate_captcha_image(text):
    try:
        width, height = 200, 80
        image = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        # Load a font (adjust the path for your environment)
        try:
            font_path = os.path.join(os.path.dirname(__file__), 'static/fonts/arial.ttf')
            font = ImageFont.truetype(font_path, 50)
        except IOError:
            font = ImageFont.load_default()

        # Add text to image
        for i in range(len(text)):
            draw.text((20 + i * 30, 10), text[i], font=font, fill=(random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)))

        # Add random lines (noise)
        for _ in range(5):
            x1 = random.randint(0, width)
            y1 = random.randint(0, height)
            x2 = random.randint(0, width)
            y2 = random.randint(0, height)
            draw.line(((x1, y1), (x2, y2)), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), width=2)

        # Slightly blur the image
        image = image.filter(ImageFilter.BLUR)

        # Save the image to a bytes buffer
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)
        
        return buffer
    except Exception as e:
        print(f"Error generating CAPTCHA image: {e}")
        return None

# View to generate and return CAPTCHA image
def captcha_image(request):
    captcha_text = request.session.get('captcha_text')
    if captcha_text:
        image_buffer = generate_captcha_image(captcha_text)
        if image_buffer:
            return HttpResponse(image_buffer, content_type='image/png')
    return HttpResponse("Error generating CAPTCHA image", status=500)

# Main index view for the form and CAPTCHA validation
def index(request):
    error_message = None

    # Handle form submission (POST request)
    if request.method == 'POST':
        entered_captcha = request.POST.get('captcha')  # Get the user-entered CAPTCHA
        session_captcha = request.session.get('captcha_text')  # Get the CAPTCHA from the session

        # Check if entered CAPTCHA exactly matches session CAPTCHA (case-sensitive comparison)
        if entered_captcha and session_captcha and entered_captcha == session_captcha:
            return redirect('success')  # Redirect to a success page if the CAPTCHA is correct
        else:
            error_message = "Incorrect CAPTCHA. Please try again."

    # Generate a new CAPTCHA if the form is not submitted or CAPTCHA was incorrect
    captcha_text = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5))
    request.session['captcha_text'] = captcha_text

    # Pass the error message to the template (if any)
    return render(request, 'index.html', {'error_message': error_message})

# Success view after correct CAPTCHA submission
def success(request):
    return HttpResponse("CAPTCHA successfully validated!")
