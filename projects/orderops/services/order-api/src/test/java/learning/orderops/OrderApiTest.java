package learning.orderops;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
class OrderApiTest {
    @Test void healthContract() { assertEquals("OK", new OrderApi().health()); }
}
