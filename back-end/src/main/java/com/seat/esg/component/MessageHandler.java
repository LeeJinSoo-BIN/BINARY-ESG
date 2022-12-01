package com.seat.esg.component;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.seat.esg.form.RequestMessageForm;
import com.seat.esg.domain.SeatStatus;
import com.seat.esg.service.MessageService;
import com.seat.esg.service.SeatService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

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

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        sessions.put(session.getId(), session);
    }

    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
        String msg = message.getPayload();

        RequestMessageForm requestMessageForm = objectMapper.readValue(msg, RequestMessageForm.class);
        int seatNum = requestMessageForm.getSeatNum();
        String messageType = requestMessageForm.getMessageType();

        switch (messageType) {
            case "REQUEST":
                messageService.createAwayRequestMessage(seatNum);
                break;
            case "CHANGE-EMPTY":
                messageService.deleteClearSeatMessage(seatNum);
                seatService.changeSeatStatus(seatNum, SeatStatus.EMPTY);
                break;
            case "CHANGE-AWAY":
                seatService.changeSeatStatus(seatNum, SeatStatus.AWAY);
                break;
            case "CHANGE-FULL":
                seatService.changeSeatStatus(seatNum, SeatStatus.FULL);
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
}
