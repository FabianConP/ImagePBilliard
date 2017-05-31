package com.imagepbilliard.imagepbilliard;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.drawable.shapes.OvalShape;
import android.support.annotation.Nullable;
import android.util.AttributeSet;
import android.view.View;

import java.util.LinkedList;
import java.util.List;

import model.Ball;
import model.BallResult;

public class GameView extends View {

    private BallResult mBallResult;
    static final int BALL_RADIO = 10;

    private List<OvalShape> mOvalBalls;

    public GameView(Context context, BallResult ballResult) {
        super(context);
        mBallResult = ballResult;
        List<Ball> balls = mBallResult.getResult();
        mOvalBalls = new LinkedList<>();

        for(Ball ball: balls){
            OvalShape ovalShape = new OvalShape();
            ovalShape.resize(BALL_RADIO, BALL_RADIO);

        }

    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
    }
}
