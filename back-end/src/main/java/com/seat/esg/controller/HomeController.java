package com.seat.esg.controller;

import com.seat.esg.domain.Message;
import com.seat.esg.domain.Seat;
import com.seat.esg.domain.SeatNumber;
import com.seat.esg.service.MessageService;
import com.seat.esg.service.SeatService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
@RequiredArgsConstructor
public class HomeController {

    private final SeatService seatService;
    private final MessageService messageService;

    @GetMapping("/")
    public String firstPage(){
        return "first";
    }

    @GetMapping("/home")
    public String home(Model model) throws Exception {
        makeSeatData(model);
        return "home";
    }

    @GetMapping("/manager")
    public String manager(Model model) {
        makeSeatData(model);
        makeMassegeData(model);
        return "manager";
    }

    private void makeSeatData(Model model) {
        List<Seat> seats = seatService.findSeats();
        SeatNumber seatNumber = seatService.countSeatNumber();
        model.addAttribute("seats", seats);
        model.addAttribute("seatNumber", seatNumber);
    }

    private void makeMassegeData(Model model) {
        List<Message> messages = messageService.findMessages();
        model.addAttribute("messages", messages);
    }
}
