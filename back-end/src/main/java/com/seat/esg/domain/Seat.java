package com.seat.esg.domain;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

@Entity
@Getter @Setter
public class Seat {

    @Id @GeneratedValue
    @Column(name = "seat_id")
    private Long id;

    private int seatNum;

    private int emptyMinute;

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
        seat.setEmptyMinute(0);
        seat.setStatus(SeatStatus.EMPTY);
        seat.setPlace(place);
        return seat;
    }

    //==비즈니스 로직==//
    /**
     * 부재중 시간 증가
     */
    public void addTime(int time) {
        this.emptyMinute += time;
    }

    /**
     * 부재중 시간 초기화
     */
    public void initTime() {
        this.emptyMinute = 0;
    }

    /**
     * 자리 상태 변경
     */
    public void changeStatus(SeatStatus status) {
        this.status = status;
    }
}
