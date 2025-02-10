use axum::{http::StatusCode, response::IntoResponse, Json};
use serde::{Deserialize, Serialize};
use serde_json::Value;

pub async fn process_data(Json(request): Json<DataRequest>) -> impl IntoResponse {
    // Calculate sums and return response

    let mut string_len = 0;
    let mut int_sum = 0;


    // Just using panics here as its not specified what to do in case of an error
    for elem in request.data {
        match elem {
            Value::Number(n) => {
                match n.as_i64() {
                    Some(x) => int_sum += x,
                    None => panic!("Number was unable to be converted to integer."),
                }
            },
            Value::String(s) => string_len += s.len(),
            _ => panic!("Shouldn't have encountered non num / string data."),
        }
    }


    let response = DataResponse {
        string_len: string_len,
        int_sum: int_sum,
    };

    (StatusCode::OK, Json(response))
}

#[derive(Deserialize)]
pub struct DataRequest {
    data: Vec<Value>,
}

#[derive(Serialize)]
pub struct DataResponse {
    string_len: usize,
    int_sum: i64,
}
