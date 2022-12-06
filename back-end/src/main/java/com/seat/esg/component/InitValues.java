package com.seat.esg.component;

import com.seat.esg.domain.Member;
import com.seat.esg.domain.MemberRole;
import com.seat.esg.service.MemberService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;

@Component
@RequiredArgsConstructor
public class InitValues {

    private final MemberService memberService;
    private final PasswordEncoder passwordEncoder;

    @PostConstruct
    public void init() throws Exception {
        Member member = new Member();
        member.setEnabled(true);
        member.setName("manager");
        member.setPassword(passwordEncoder.encode("123"));
        member.setRole(MemberRole.MANAGER);
        memberService.join(member);
    }


}
