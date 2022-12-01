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

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "place_id")
    private Place place;

    //==연관관계 메서드==//
    public void setPlace(Place place) {
        this.place = place;
        place.getSeats().add(this);
    }

    //==생성 메서드==//
    public static Seat createSeat(int SeatNum, Place place) {
        Seat seat = new Seat();
        seat.setSeatNum(SeatNum);
        seat.setAwayMinute(0);
        seat.setStatus(SeatStatus.EMPTY);
        seat.setPlace(place);
        return seat;
    }

    public int addAwayMinute(int minute) {
        this.awayMinute += minute;
        return this.awayMinute;
    }

    public void initAwayMinute() {
        this.awayMinute = 0;
    }
}
