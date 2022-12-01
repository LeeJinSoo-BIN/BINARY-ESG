package com.seat.esg.domain;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Entity
@Getter @Setter
public class Message {

    @Id
    @GeneratedValue
    @Column(name = "message_id")
    private Long id;

    private int seatNum;
    private String sendTime;

    //==생성 메서드==//
    public static Message createMessage(int seatNum) {
        Message message = new Message();
        message.setSeatNum(seatNum);
        String formatTime = '[' + formatTime(LocalDateTime.now()) + ']';
        message.setSendTime(formatTime);
        return message;
    }


    public static String formatTime(LocalDateTime time) {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm");
        return time.format(formatter);
    }
}
