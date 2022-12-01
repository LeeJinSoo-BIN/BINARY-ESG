package com.seat.esg.service;

import com.seat.esg.domain.Message;
import com.seat.esg.repository.MessageRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class MessageService {

    private final MessageRepository messageRepository;

    @Transactional
    public Long createAwayRequestMessage(int seatNum) {
        Message message = Message.createMessage(seatNum);
        messageRepository.save(message);
        return message.getId();
    }

    @Transactional
    public void deleteClearSeatMessage(int seatNum) {
        if (!messageRepository.findBySeatNum(seatNum).isEmpty()) {
            messageRepository.removeBySeatNum(seatNum);
        }
    }

    public List<Message> findMessages() {
        return messageRepository.findAll();
    }
}
