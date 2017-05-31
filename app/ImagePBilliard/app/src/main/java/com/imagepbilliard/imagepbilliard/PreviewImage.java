package com.imagepbilliard.imagepbilliard;

import android.app.ActionBar;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.ByteArrayOutputStream;
import java.util.List;

import model.APIService;
import model.ApiUtils;
import model.Ball;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class PreviewImage extends AppCompatActivity {

    private ImageView mImgPreview;
    private FloatingActionButton mBtnSend;

    private Bitmap mBitmapImage;
    private APIService mAPIService;

    static final String TAG = PreviewImage.class.getSimpleName();

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

        mAPIService = ApiUtils.getAPIService();

        mBtnSend = (FloatingActionButton) findViewById(R.id.pv_send);

        mBtnSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Toast.makeText(getApplicationContext(), "Sending",  Toast.LENGTH_SHORT).show();
                String encoded = transformImageBase64(mBitmapImage);
                sendPostRequest(encoded);
            }
        });
    }

    private String transformImageBase64(Bitmap bitmap){
        ByteArrayOutputStream baos = new ByteArrayOutputStream();
        bitmap.compress(Bitmap.CompressFormat.JPEG, 100, baos); //bm is the bitmap object
        byte[] byteArrayImage = baos.toByteArray();
        String encodedImage = Base64.encodeToString(byteArrayImage, Base64.DEFAULT);
        return encodedImage;
    }

    private void sendPostRequest(String img_str) {
        mAPIService.sendImage(img_str).enqueue(new Callback<Ball>() {
            @Override
            public void onResponse(Call<Ball> call, Response<Ball> response) {
                if(response.isSuccessful()){
                    Intent intentSuggestion = new Intent(getApplicationContext(), Suggestion.class);
                    intentSuggestion.putExtra("cnt", response.body().toString());
                    startActivity(intentSuggestion);
                }
            }

            @Override
            public void onFailure(Call<Ball> call, Throwable t) {
                Log.e(TAG, "Unable to submit post to API." + t.getMessage());
            }
        });
    }

}
