package model;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.Field;
import retrofit2.http.FormUrlEncoded;
import retrofit2.http.POST;

public interface APIService {

    @POST("/")
    @FormUrlEncoded
    Call<BallResult> sendImage(@Field("img_str") String img_str);
}
