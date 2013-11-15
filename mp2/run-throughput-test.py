
import os, time, tailer, scipy, sys

def main():
    
    loss_patterns = [ '5', '10', '20' ]
    file_names = ['test3.txt', 'test5.txt', 'test6.txt']
    file_sizes = [1000, 100000, 1000000]
    receiver_domain_name = 'localhost'
    receiver_port = '1234'
    delay_time = 0.25
    number_experiments = 100

    for loss_pattern in loss_patterns:
        # loss pattern 5
        print >> sys.stderr, "Loss pattern", loss_pattern
        results = [loss_pattern]
        for i in range(0,len(file_names)):
            time_reqs = []
            file_size = file_sizes[i]
            file_name = file_names[i]
            for experiment_id in range(0, number_experiments):
                os.system('python receiver.py ' + receiver_port + ' ' + loss_pattern  + ' > temp &')
                # wait 1 second 
                time.sleep(delay_time)
                os.system('python sender.py ' + file_name + ' ' + receiver_domain_name + ' ' + receiver_port)
                time.sleep(delay_time)

                with open('trace') as tf:
                    last_line = tailer.tail(tf, 1)
                time_req = float(last_line[0].split(' ')[0])
                time_reqs.append(time_req)
                print >> sys.stderr, experiment_id, "File", file_name, "Size", file_size, "Time", time_req

            mean_time = scipy.mean(time_reqs)
            std_time = scipy.std(time_reqs)
            min_time = mean_time - std_time
            max_time = mean_time + std_time
            mean_throughput = file_size * 8000.0 / mean_time
            max_throughput = file_size * 8000.0 / min_time
            min_throughput = file_size * 8000.0 / max_time
            this_result = [ str(mean_throughput), str(min_throughput), str( max_throughput)]
            results += this_result
            print >> sys.stderr, ' '.join(this_result)
        print ' '.join(results)

if __name__ == '__main__':
    main()
