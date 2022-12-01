package com.seat.esg.domain;

import lombok.Getter;
import lombok.Setter;
import org.hibernate.annotations.DynamicUpdate;

import javax.persistence.*;

@Entity
@Getter @Setter
@DynamicUpdate
public class Seat {

    @Id @GeneratedValue
    @Column(name = "seat_id")
    private Long id;

    private int seatNum;

    private int awayMinute;

    @Enumerated(EnumType.STRING)
    private SeatStatus status;

    public int addAwayMinute(int minute) {
        this.awayMinute += minute;
        return this.awayMinute;
    }

    public void initAwayMinute() {
        this.awayMinute = 0;
    }
}
