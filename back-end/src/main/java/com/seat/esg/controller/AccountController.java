package com.seat.esg.controller;

import com.seat.esg.domain.Member;
import com.seat.esg.domain.MemberRole;
import com.seat.esg.service.MemberService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import javax.validation.Valid;

@Controller
@RequestMapping("/account")
@RequiredArgsConstructor
public class AccountController {

    private final MemberService memberService;
    private final PasswordEncoder passwordEncoder;

    @GetMapping("/login")
    public String login() {
        return "account/login";
    }

    @GetMapping("/register")
    public String registerForm(Model model) {
        model.addAttribute("memberForm", new MemberForm());
        return "account/register";
    }

    @PostMapping("/register")
    public String register(@Valid MemberForm form, BindingResult result) {
        if (result.hasErrors()) {
            return "account/register";
        }

        String encodedPassword = passwordEncoder.encode(form.getPassword());
        Member member = new Member();
        member.setName(form.getName());
        member.setPassword(encodedPassword);
        member.setRole(MemberRole.USER);
        member.setEnabled(true);

        memberService.join(member);

        return "redirect:/";
    }
}
