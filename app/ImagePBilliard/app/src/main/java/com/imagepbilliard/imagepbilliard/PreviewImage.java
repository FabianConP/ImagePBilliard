package com.imagepbilliard.imagepbilliard;

import android.app.ActionBar;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.ByteArrayOutputStream;

public class PreviewImage extends AppCompatActivity {

    private ImageView mImgPreview;
    private FloatingActionButton mBtnSend;

    private Bitmap mBitmapImage;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_preview_image);

        View decorView = getWindow().getDecorView();
        // Hide the status bar.
        int uiOptions = View.SYSTEM_UI_FLAG_FULLSCREEN;
        decorView.setSystemUiVisibility(uiOptions);

        mImgPreview = (ImageView) findViewById(R.id.pv_image);

        Intent intent = getIntent();
        byte[] byteArray = intent.getByteArrayExtra(MainActivity.IMAGE_EXTRA);
        mBitmapImage = BitmapFactory.decodeByteArray(byteArray, 0, byteArray.length);

        mImgPreview.setImageBitmap(mBitmapImage);

        mBtnSend = (FloatingActionButton) findViewById(R.id.pv_send);

        mBtnSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(getApplicationContext(), "Sending",  Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void transformImageBase64(Bitmap bitmap){
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, baos); //bm is the bitmap object
        byte[] byteArrayImage = baos.toByteArray();
        String encodedImage = Base64.encodeToString(byteArrayImage, Base64.DEFAULT);

    }

    private void sendPostRequest(String img_str){

    }

}
