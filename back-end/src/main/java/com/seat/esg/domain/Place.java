package com.seat.esg.domain;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Entity
@Getter @Setter
public class Place {
    @Id
    @GeneratedValue
    @Column(name = "place_id")
    private Long id;

    private String name;

    @OneToMany(mappedBy = "place")
    private List<Seat> seats = new ArrayList<>();
}
