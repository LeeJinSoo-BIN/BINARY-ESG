package com.seat.esg.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.seat.esg.form.ResponseFlaskForm;
import com.seat.esg.domain.SeatStatus;
import com.seat.esg.controller.FlaskController;
import lombok.RequiredArgsConstructor;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.List;

@Service
@RequiredArgsConstructor
public class RequestService {

    private final FlaskController flaskController;
    private final ObjectMapper objectMapper;
    private final SeatService seatService;

    @Scheduled(cron = "0/30 * 9-22 ? * MON-FRI")
    public void requestToFlask() throws IOException {
        String test = flaskController.responseFromFlask();
        ResponseFlaskForm responseFlaskForm = objectMapper.readValue(test, ResponseFlaskForm.class);
        List<String> status = responseFlaskForm.getStatus();

        for (int i = 0; i < status.size(); i++) {
            SeatStatus seatStatus = seatService.changeStringStatusToEnum(status.get(i));
            seatService.updateStatus(i + 1, seatStatus);
        }
    }
}
