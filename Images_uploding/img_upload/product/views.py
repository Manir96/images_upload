from django.shortcuts import get_object_or_404, render
from product.serializers import ProductSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from product.models import Product
from rest_framework import status
import face_recognition as fr  # To recognize faces
import cv2  # To read and display images
import os
import uuid

# Create your views here.
#"D:\Internship\Images_uploding\img_upload\product\dlib_cmake_library\dlib\dlib\Install-dlib-main"
def ima_upload(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        upload_image = request.FILES.get('upload_image')
        image_path = 'D:\\Internship\\Images_uploding\\img_upload\\media\\'+str(upload_image)
        faces_folder = 'D:\\Internship\\Images_uploding\\img_upload\\media\\image'
        def get_face_encodings():
            face_names = os.listdir(faces_folder)
            face_encodings = []
            for i, name in enumerate(face_names):
                face = fr.load_image_file(f"{faces_folder}/{name}")
                face_encodings.append(fr.face_encodings(face)[0])
                face_names[i] = name.split(".")[0]
            return face_encodings, face_names

        face_encodings, face_names = get_face_encodings()

        # Load the image for face recognition
        image = fr.load_image_file(image_path)

        # Convert the image to RGB, as face_recognition library requires RGB format
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Find face locations in the image
        face_locations = fr.face_locations(rgb_image)

        # Encode the faces found in the image
        unknown_encodings = fr.face_encodings(rgb_image, face_locations)

        for face_encoding_test, face_location in zip(unknown_encodings, face_locations):
            result = fr.compare_faces(face_encodings, face_encoding_test, 0.4)
            if True in result:
                name = face_names[result.index(True)]
                top, right, bottom, left = face_location
                cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(image, name, (left, bottom + 20), font, 0.8, (255, 255, 255), 1)
            else:
                top, right, bottom, left = face_location
                cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(image, "unknown", (left, bottom + 20), font, 0.8, (255, 255, 255), 1)

        # Display the image with face recognition results
        random_filename = str(uuid.uuid4()) + ".jpg"
        image_path3 = 'D:\\Internship\\Images_uploding\\img_upload\\media\\'+random_filename
        print(random_filename)
        # Save the recognized image with the random name
        cv2.imwrite(image_path3, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        
        # cv2.imshow("Image with Face Recognition", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        if name and upload_image:
            product = Product(name=name, product_image=random_filename)
            # print(product.product_image)
            product.save()
             
    last_product = Product.objects.last()
    
    print(last_product.product_image)
    return render(request, 'index.html', {'last_product': last_product})

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(user)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        
    def update(self, request, pk=None):
        Product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)