package kr.co.littleriders.backend.domain.shuttle;

import kr.co.littleriders.backend.domain.shuttle.entity.ShuttleChildRide;

public interface ShuttleChildRideService {

    void save(ShuttleChildRide shuttleChildRide);

    ShuttleChildRide findByShuttleId(long shuttleId);

    void delete(ShuttleChildRide shuttleChildRide);
}