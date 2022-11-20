package com.seat.esg.repository;

import com.seat.esg.domain.Place;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Repository;

import javax.persistence.EntityManager;
import java.util.List;

@Repository
@RequiredArgsConstructor
public class PlaceRepository {

    private final EntityManager em;

    public void save(Place place) {
        em.persist(place);
    }

    public Place findOne(Long id) {
        return em.find(Place.class, id);
    }

    public List<Place> findAll() {
        return em.createQuery("select p from Place p", Place.class)
                .getResultList();
    }

    public List<Place> findByName(String name) {
        return em.createQuery("select p from Place p where p.name = :name", Place.class)
                .setParameter("name", name)
                .getResultList();
    }
}
