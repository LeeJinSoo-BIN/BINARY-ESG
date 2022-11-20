package com.seat.esg.repository;

import com.seat.esg.domain.Member;
import com.seat.esg.domain.Seat;
import com.seat.esg.domain.SeatStatus;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import javax.persistence.EntityManager;
import java.util.List;

@Repository
@RequiredArgsConstructor
public class SeatRepository {

    private final EntityManager em;

    public void save(Seat seat) {
        em.persist(seat);
    }

    public Seat findOne(Long id) {
        return em.find(Seat.class, id);
    }

    public List<Seat> findAll() {
        return em.createQuery("select s from Seat s", Seat.class)
                .getResultList();
    }

    public List<Seat> findByStatus(SeatStatus status) {
        return em.createQuery("select s from Seat s where s.status = :status", Seat.class)
                .setParameter("status", status)
                .getResultList();
    }
}
