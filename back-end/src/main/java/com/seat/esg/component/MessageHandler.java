package com.seat.esg.component;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.seat.esg.controller.FlaskController;
import com.seat.esg.domain.Seat;
import com.seat.esg.form.RequestMessageForm;
import com.seat.esg.domain.SeatStatus;
import com.seat.esg.form.ResponseFlaskForm;
import com.seat.esg.service.MessageService;
import com.seat.esg.service.SeatService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Slf4j
@Component
@RequiredArgsConstructor
public class MessageHandler extends TextWebSocketHandler {

    private final ObjectMapper objectMapper;
    private final Map<String, WebSocketSession> sessions = new ConcurrentHashMap<>();
    private final MessageService messageService;
    private final SeatService seatService;
    private final FlaskController flaskController;

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        sessions.put(session.getId(), session);
    }

    @Override
    @Transactional
    protected void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
        String msg = message.getPayload();

        RequestMessageForm requestMessageForm = objectMapper.readValue(msg, RequestMessageForm.class);
        int seatNum = requestMessageForm.getSeatNum();
        String messageType = requestMessageForm.getMessageType();
        Seat seat = seatService.findSeat(seatNum);

        switch (messageType) {
            case "REQUEST":
                messageService.createAwayRequestMessage(seatNum);
                break;
            case "CHANGE-EMPTY":
                seatService.updateSeatStatus(seatNum, SeatStatus.EMPTY);
                break;
            case "CHANGE-AWAY":
                seatService.updateSeatStatus(seatNum, SeatStatus.AWAY);
                break;
            case "CHANGE-FULL":
                seatService.updateSeatStatus(seatNum, SeatStatus.FULL);
                break;
        }


        sessions.forEach((sessionId, sessionInMap) -> {
            try {
                sessionInMap.sendMessage(new TextMessage(""));
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        sessions.remove(session.getId(), session);
    }

//    @Scheduled(cron = "0/30 * 9-22 ? * MON-FRI")
    @Scheduled(cron = "0/30 * * ? * MON-FRI")
    public void requestToFlask() throws IOException {
        String test = flaskController.responseFromFlask();
        ResponseFlaskForm responseFlaskForm = objectMapper.readValue(test, ResponseFlaskForm.class);
        List<String> status = responseFlaskForm.getStatus();

        for (int i = 0; i < seatService.findSeats().size() || i < status.size(); i++) {
            SeatStatus seatStatus = seatService.changeStringStatusToEnum(status.get(i));
            seatService.updateStatusByNowStatus(i + 1, seatStatus);
        }

        sessions.forEach((sessionId, sessionInMap) -> {
            try {
                sessionInMap.sendMessage(new TextMessage(""));
            } catch (Exception e) {
                e.printStackTrace();
            }
        });
    }
}
