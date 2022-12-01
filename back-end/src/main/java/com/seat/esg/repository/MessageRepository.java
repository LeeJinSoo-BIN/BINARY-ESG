package com.seat.esg.repository;

import com.seat.esg.domain.Message;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import javax.persistence.EntityManager;
import java.util.List;

@Repository
@RequiredArgsConstructor
public class MessageRepository {

    private final EntityManager em;

    public void save(Message message) {
        em.persist(message);
    }

    public List<Message> findAll() {
        return em.createQuery("select m from Message m", Message.class)
                .getResultList();
    }

    public List<Message> findBySeatNum(int seatNum) {
        return em.createQuery("select m from Message m where m.seatNum = :seatNum", Message.class)
                .setParameter("seatNum", seatNum)
                .getResultList();
    }

    public void removeBySeatNum(int seatNum) {
        em.createQuery("delete from Message where seatNum = :seatNum")
                .setParameter("seatNum", seatNum)
                .executeUpdate();
    }
}
