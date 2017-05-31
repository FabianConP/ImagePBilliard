package com.imagepbilliard.imagepbilliard;

import android.content.Intent;
import android.graphics.Point;
import android.media.Image;
import android.support.v7.app.ActionBar;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.Display;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.Toast;

import java.util.LinkedList;
import java.util.List;

import model.Ball;
import model.BallResult;

public class Suggestion extends AppCompatActivity {

    private BallResult mBallResult;
    private List<ImageView> mBalls;

    private RelativeLayout mGameLayout;

    private int WIDTH;
    private int HEIGHT;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_suggestion);

        View decorView = getWindow().getDecorView();
        // Hide the status bar.
        int uiOptions = View.SYSTEM_UI_FLAG_FULLSCREEN;
        decorView.setSystemUiVisibility(uiOptions);

        mGameLayout = (RelativeLayout) findViewById(R.id.game);
        mGameLayout.setLayoutParams(new RelativeLayout.LayoutParams(mGameLayout.getHeight() / 2, ViewGroup.LayoutParams.FILL_PARENT));
        mGameLayout.setLayoutParams(new RelativeLayout.LayoutParams(ViewGroup.LayoutParams.FILL_PARENT, ViewGroup.LayoutParams.FILL_PARENT));
        mGameLayout.requestLayout();

        Intent intent = getIntent();
        mBallResult = (BallResult) intent.getSerializableExtra(PreviewImage.BALL_RESULT);
        Toast.makeText(getApplicationContext(), mBallResult.toString(), Toast.LENGTH_SHORT).show();
    }

    @Override
    protected void onStart() {
        super.onStart();
        HEIGHT = mGameLayout.getHeight();
        WIDTH = mGameLayout.getWidth();

        HEIGHT = getWindowManager().getDefaultDisplay().getHeight();
        WIDTH = getWindowManager().getDefaultDisplay().getWidth();

        List<Ball> balls = mBallResult.getResult();

        mBalls = new LinkedList<>();
        mBalls.add((ImageView) findViewById(R.id.ball1));
        mBalls.add((ImageView) findViewById(R.id.ball2));
        mBalls.add((ImageView) findViewById(R.id.ball3));

        for(int i = 0; i < balls.size(); i++){
            Ball ball = balls.get(i);
            ImageView image = mBalls.get(i);
            setPosition(ball, image);
        }
    }

    private void setPosition(Ball ball, ImageView image){
        int x = ball.getY(), y = ball.getX(), a = ball.getAngle();
        image.setRotation(a);
        double fx = WIDTH / 500.0;
        double fy = HEIGHT / 1000.0;
        x = (int) Math.round(x * fx);
        y = (int) Math.round(y * fy);
        ViewGroup.MarginLayoutParams marginParams = new ViewGroup.MarginLayoutParams(image.getLayoutParams());
        marginParams.setMargins(x, y, 0, 0);
        RelativeLayout.LayoutParams layoutParams = new RelativeLayout.LayoutParams(marginParams);
        image.setLayoutParams(layoutParams);
        image.requestLayout();
    }
}
