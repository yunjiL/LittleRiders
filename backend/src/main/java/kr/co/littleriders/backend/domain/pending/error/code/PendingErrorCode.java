package kr.co.littleriders.backend.domain.pending.error.code;

import kr.co.littleriders.backend.global.error.code.LittleRidersErrorCode;
import org.springframework.http.HttpStatus;


public enum PendingErrorCode implements LittleRidersErrorCode {


    NOT_FOUND(HttpStatus.NOT_FOUND, "001", "대기 기록을 찾을수 없습니다"),
    ILLEGAL_ACADEMY(HttpStatus.BAD_REQUEST, "002", "요청 매개변수가 유효하지 않습니다");


    PendingErrorCode(HttpStatus status, String code, String message) {
        this.status = status;
        this.code = "PENDING_" + code;
        this.message = message;
    }

    private final HttpStatus status;
    private final String code;
    private final String message;


    @Override
    public HttpStatus getStatus() {
        return status;
    }

    @Override
    public String getCode() {
        return code;
    }

    @Override
    public String getMessage() {
        return message;
    }
}