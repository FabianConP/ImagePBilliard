package com.imagepbilliard.imagepbilliard;

import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.provider.MediaStore;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;

import java.io.ByteArrayOutputStream;

import util.Util;

public class MainActivity extends AppCompatActivity {

    static final int REQUEST_IMAGE_CAPTURE = 1;
    static final int REQUEST_IMAGE_SELECTOR = 2;
    static final String IMAGE_EXTRA = "IMAGE_EXTRA";

    private FloatingActionButton mButtonGallery;
    private FloatingActionButton mButtonCamera;
    private ImageView mImgLogo;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mButtonGallery = (FloatingActionButton) findViewById(R.id.am_gallery);
        mButtonCamera = (FloatingActionButton) findViewById(R.id.am_camera);
        mImgLogo = (ImageView) findViewById(R.id.am_logo);

        mButtonGallery.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                dispatchSelectPictureIntent();
            }
        });

        mButtonCamera.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                dispatchTakePictureIntent();
            }
        });
    }

    private void dispatchTakePictureIntent() {
        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (takePictureIntent.resolveActivity(getPackageManager()) != null)
            startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
    }



    private void dispatchSelectPictureIntent(){
        Intent galleryIntent = new Intent(Intent.ACTION_PICK,
                android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
        if(galleryIntent.resolveActivity(getPackageManager()) != null)
            startActivityForResult(galleryIntent , REQUEST_IMAGE_SELECTOR);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        try{
            if(resultCode == RESULT_OK && data != null) {
                Bitmap imageBitmap = null;
                switch (requestCode) {
                    case REQUEST_IMAGE_CAPTURE:
                        Bundle extras = data.getExtras();
                        imageBitmap = (Bitmap) extras.get("data");
                        break;
                    case REQUEST_IMAGE_SELECTOR:
                        Uri selectedImage = data.getData();
                        String[] filePathColumn = {MediaStore.Images.Media.DATA};

                        Cursor cursor = getContentResolver().query(selectedImage, filePathColumn, null, null, null);
                        cursor.moveToFirst();

                        int columnIndex = cursor.getColumnIndex(filePathColumn[0]);
                        String filePath = cursor.getString(columnIndex);
                        cursor.close();

                        imageBitmap = BitmapFactory.decodeFile(filePath);
                        break;
                }
                if(imageBitmap != null) {
                    imageBitmap = Util.scaleDownBitmap(imageBitmap, 100, getApplicationContext());
                    startPreviewImageIntent(imageBitmap);
                }
            }
        }catch (Exception e){
            Log.e(MainActivity.class.getSimpleName(), e.getMessage());
        }
    }

    private void startPreviewImageIntent(Bitmap bitmap){
        ByteArrayOutputStream stream = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.PNG, 100, stream);
        byte[] byteArray = stream.toByteArray();

        Intent previewIntent = new Intent(this, PreviewImage.class);
        previewIntent.putExtra(IMAGE_EXTRA, byteArray);
        startActivity(previewIntent);
    }
}
