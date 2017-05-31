package model;

import java.io.Serializable;
import java.util.List;

public class BallResult implements Serializable{
    private List<Ball> result;

    public BallResult(List<Ball> result) {
        this.result = result;
    }

    public List<Ball> getResult() {
        return result;
    }

    public void setResult(List<Ball> result) {
        this.result = result;
    }

    @Override
    public String toString() {
        return "BallResult{" +
                "result=" + result.toString() +
                '}';
    }
}
