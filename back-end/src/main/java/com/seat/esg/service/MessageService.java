package com.seat.esg.service;

import com.seat.esg.domain.Message;
import com.seat.esg.domain.SeatStatus;
import com.seat.esg.repository.MessageRepository;
import com.seat.esg.repository.SeatRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class MessageService {

    private final MessageRepository messageRepository;
    private final SeatRepository seatRepository;

    @Transactional
    public void createAwayRequestMessage(int seatNum) {
        Message message = Message.createMessage(seatNum);
        messageRepository.save(message);
    }

    @Transactional
    public void deleteClearSeatMessage(int seatNum) {
        if (!messageRepository.findBySeatNum(seatNum).isEmpty() && !(seatRepository.findOneBySeatNum(seatNum).getStatus() == SeatStatus.AWAY)) {
            messageRepository.removeBySeatNum(seatNum);
        }
    }

    public List<Message> findMessages() {
        return messageRepository.findAll();
    }
}
