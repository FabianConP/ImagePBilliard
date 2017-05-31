package model;

public class ApiUtils {
    private ApiUtils(){}

    public static final String BASE_URL = "http://192.168.1.15:5000/";

    public static APIService getAPIService() {

        return RetrofitClient.getClient(BASE_URL).create(APIService.class);
    }

}
