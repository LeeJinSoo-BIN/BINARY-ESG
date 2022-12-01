package com.seat.esg.service;

import com.seat.esg.domain.SeatNumber;
import com.seat.esg.domain.Seat;
import com.seat.esg.domain.SeatStatus;
import com.seat.esg.repository.SeatRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
@Transactional(readOnly = true)
@RequiredArgsConstructor
public class SeatService {

    private final int cycle = 10;

    private final SeatRepository seatRepository;

    @Transactional
    public void saveSeat(Seat seat) {
        seatRepository.save(seat);
    }

    public List<Seat> findSeats() {
        return seatRepository.findAll();
    }

    public Seat findOne(Long seatId) {
        return seatRepository.findOne(seatId);
    }

    public SeatNumber countSeatNumber() {
        SeatNumber seatNumber = new SeatNumber();
        seatNumber.setEmptySeat(seatRepository.findByStatus(SeatStatus.EMPTY).size());
        seatNumber.setAwaySeat(seatRepository.findByStatus(SeatStatus.AWAY).size());
        seatNumber.setFullSeat(seatRepository.findByStatus(SeatStatus.FULL).size());
        return seatNumber;
    }

    @Transactional
    public void changeSeatStatus(int seatNum, SeatStatus status) {
        Seat seat = seatRepository.findOneBySeatNum(seatNum);
        seat.setStatus(status);
    }

    public SeatStatus changeStringStatusToEnum(String status) {
        switch (status) {
            case "EMPTY":
                return SeatStatus.EMPTY;
            case "AWAY":
                return SeatStatus.AWAY;
            case "FULL":
                return SeatStatus.FULL;
        }
        return null;
    }

    @Transactional
    public void updateStatus(int seatNum, SeatStatus nowStatus) {
        Seat seat = seatRepository.findOneBySeatNum(seatNum);
        if (nowStatus == SeatStatus.AWAY) {
            int awayMinute = seat.addAwayMinute(cycle);
            if (awayMinute > 30) {
                seat.setStatus(SeatStatus.AWAY);
            } else {
                seat.setStatus(SeatStatus.FULL);
            }
        } else {
            seat.initAwayMinute();
            seat.setStatus(nowStatus);
        }
    }
}
