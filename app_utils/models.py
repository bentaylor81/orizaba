from django.db import models

class PrintProcess(models.Model):
    process_id = models.IntegerField(primary_key=True)
    process_name = models.CharField(max_length=200, blank=True, null=True)
    process_printer = models.ForeignKey('printer', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.process_name) + ' | ' + str(self.process_printer)

class Printer(models.Model):
    CHOICES = [
        ('Ben Laptop - 331090', 'Ben Laptop'),
        ('Label Desktop - 265194', 'Label Desktop'),
        ('Jodie Desktop - 318172', 'Jodie Desktop'),  
        ('Nick Desktop', 'Nick Desktop'),      
        ('Warehouse Desktop - 332120', 'Warehouse Desktop'),          
    ]
    printer_name = models.CharField(max_length=200, blank=True, null=True)
    printnode_id = models.PositiveIntegerField(blank=True, default=0) 
    computer_control = models.CharField(max_length=200, choices=CHOICES, blank=True, null=True)

    def __str__(self):
        return str(self.printer_name) + ' | ' + str(self.printnode_id) + ' | ' + str(self.computer_control)

    class Meta:
        ordering = ["computer_control", "printer_name"]
    
class ApiLog(models.Model):
    api_service = models.CharField(max_length=200, blank=True, null=True) 
    response_code = models.CharField(max_length=200, blank=True, null=True)
    response_text = models.CharField(max_length=5000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    process = models.CharField(max_length=200, blank=True, null=True) 

    def __str__(self):
        return str(self.id) + ' | ' + str(self.response)

    class Meta:
        ordering = ["-id"]