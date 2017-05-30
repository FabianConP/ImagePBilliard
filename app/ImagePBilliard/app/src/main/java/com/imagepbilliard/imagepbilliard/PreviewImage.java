package com.imagepbilliard.imagepbilliard;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;

public class PreviewImage extends AppCompatActivity {

    private ImageView mImgPreview;
    private FloatingActionButton mBtnSend;

    private Bitmap mBitmapImage;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_preview_image);

        View decorView = getWindow().getDecorView();
        // Calling setSystemUiVisibility() with a value of 0 clears
        // all flags.
                decorView.setSystemUiVisibility(0);

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
}
