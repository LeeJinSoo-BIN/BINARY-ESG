package com.seat.esg.controller;

import com.seat.esg.domain.Seat;
import com.seat.esg.domain.SeatStatus;
import com.seat.esg.repository.SeatRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
@RequiredArgsConstructor
public class HomeController {

    private final SeatRepository seatRepository;

    @GetMapping("/")
    public String home(Model model) {
        make(model);
        return "home";
    }

    @GetMapping("/manager")
    public String manager(Model model) {
        make(model);
        return "manager";
    }

    private void make(Model model) {
        List<Seat> seats = seatRepository.findAll();
        int awaySize = seatRepository.findByStatus(SeatStatus.AWAY).size();
        int emptySize = seatRepository.findByStatus(SeatStatus.EMPTY).size();
        int fullSize = seatRepository.findByStatus(SeatStatus.FULL).size();
        model.addAttribute("seats", seats);
        model.addAttribute("awaySize", awaySize);
        model.addAttribute("emptySize", emptySize);
        model.addAttribute("fullSize", fullSize);
    }
}
