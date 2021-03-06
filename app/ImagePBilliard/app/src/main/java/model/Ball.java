package model;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

import java.io.Serializable;

public class Ball implements Serializable{

    @SerializedName("y")
    @Expose
    private Integer y;
    @SerializedName("x")
    @Expose
    private Integer x;
    @SerializedName("angle")
    @Expose
    private Integer angle;

    public Integer getY() {
        return y;
    }

    public void setY(Integer y) {
        this.y = y;
    }

    public Integer getX() {
        return x;
    }

    public void setX(Integer x) {
        this.x = x;
    }

    public Integer getAngle() {
        return angle;
    }

    public void setAngle(Integer angle) {
        this.angle = angle;
    }

    @Override
    public String toString() {
        return "Ball{" +
                "x=" + x +
                ", y=" + y +
                ", angle=" + angle +
                '}';
    }
}