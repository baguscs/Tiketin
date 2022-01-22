import csv
from datetime import datetime

def tiket():
    #input data cari tiket
    asal = input('\nKota Asal : ').capitalize()
    tujuan = input('Kota Tujuan : ').capitalize()
    qty = int(input('Jumlah Penumpang : '))
    flay = input('Tanggal Keberangkatan : ')
    print()

    #lokasi file database
    file_tiket = "database/tiket_pesawat.txt"
    file_hotel = 'database/harga_hotel.txt'

    #validasi lokasi file tiket
    try:
        #membuka file tiket
        myFile = open(file_tiket)
        look = csv.DictReader(myFile, delimiter='\t')   
        print('\nHasil Pencarian Tiket :')
        count = 1
        find = False
        harga = []
        maskapai = []
        print("No.  Maskapai\tRute Penerbangan\t Harga Tiket")
        print("_" * 55)

        #menampilkan hasil rekomendasi tiket berdasarkan asal dan tujuan 
        for data in look:
            if data['Asal'] == asal and data['Tujuan'] == tujuan:
                find = True
                print(f"{count}.  {data['Maskapai']}\t{data['Asal']} - {data['Tujuan']}\t","Rp. {:3,.0f}".format(int(data['Harga'])))
                count +=1
                #memasukkan data yang tersaring ke dalam list
                harga.append(data['Harga'])
                maskapai.append(data['Maskapai'])

        #validasi pencarian data tiket
        if find == False:
            print('Rute yang anda cari tidak ditemukan')
        else:
            pict = int(input('\nPilihan Tiket : '))

            #menentukan harga tiket bedasarkan pilihan
            if pict > len(harga):
                price = False
            else:
                price = harga[pict-1]
                pilih_maskapai = maskapai[pict-1]          
                ppn = int(price) * 10/100
                total = (qty * int(price)) + ppn

                #menformat uang
                format_uang = '{:3,.0f}'.format(int(price))
                format_total = 'Rp. {:3,.2f}'.format(int(total))

                print(f'Total Harga Tiket: ({qty} x {format_uang}) + 10% = Rp. {format_total}\n')

                try:
                    with open(file_hotel, 'r') as myHotel:
                            load_hotel = csv.DictReader(myHotel, delimiter='\t')
                            harga_hotel = []
                            for show in load_hotel:
                                if show['Kota'] == tujuan:
                                    harga_hotel.append({
                                        "A": show['Hotel A'],
                                        "B": show['Hotel B'],
                                        "C": show['Hotel C'],
                                        "D": show['Hotel D'],
                                        "E": show['Hotel E']
                                    })
                                    
                            print('\nRekomendasi Tempat Menginap : ')
                            for query in harga_hotel:
                                print(f"Hotel A\t\tRp. {query['A']}")
                                print(f"Hotel B\t\tRp. {query['B']}")
                                print(f"Hotel C\t\tRp. {query['C']}")
                                print(f"Hotel D\t\tRp. {query['D']}")
                                print(f"Hotel E\t\tRp. {query['E']}")
                            
                            pilih_hotel = input("\nPilih hotel Anda: ").upper()
                            hotel = harga_hotel[0][pilih_hotel]
                            total_bayar = total + float(hotel.replace(',', ''))
                            print("\nTotal Biaya :")
                            print(f"{format_total} + Rp.{hotel} = ", "Rp. {:3,.2f}".format(int(total_bayar)))

                    #mengambil waktu saat ini
                    today = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')

                    #lokasi file database history tiket dan hotel
                    fileHistoryTiket = 'database/history_tiket.csv'
                    fileHistoryHotel = 'database/history_hotel.csv'

                    #validasi lokasi history tiket
                    try:
                        #membuka file history tiket dengan mode menulis data baru
                        historyTiket = open(fileHistoryTiket, 'a', newline='')
                        newHistoryTiket = csv.writer(historyTiket)

                        #menambah data history tiket baru
                        newHistoryTiket.writerow([pilih_maskapai,asal,tujuan,price,flay,qty,today])
                        historyTiket.close
                    except IOError:    
                        print('File',fileHistoryTiket,'Tidak Ditemukan')

                    #validasi lokasi history hotel    
                    try:
                        #membuka file history hotel dengan mode menulis data baru
                        historyHotel = open(fileHistoryHotel, 'a', newline='')
                        newHistoryHotel = csv.writer(historyHotel)

                        #menambah data history hotel baru
                        newHistoryHotel.writerow([pilih_hotel,hotel,today])
                        historyHotel.close
                    except IOError:
                        print('File',fileHistoryHotel,'Tidak Ditemukan')
                except IOError:
                    print('File',file_hotel,'Tidak Ditemukan')
    except IOError:
        print('File',file_tiket,'Tidak Ditemukan')
            

def history():
    #lokasi file history tiket dan hotel
    fileHistoryTiket = 'database/history_tiket.csv'
    fileHistoryHotel = 'database/history_hotel.csv'

    #validasi lokasi file history
    try:
        #membuka file history tiket
        openFileTiket = open(fileHistoryTiket)
        showTiket = csv.DictReader(openFileTiket, delimiter=',')

        #menampilkan data history tiket
        for data in showTiket:
            #membuka file history hotel
            openFileHotel = open(fileHistoryHotel)
            showHotel = csv.DictReader(openFileHotel, delimiter=',')

            print(f"========== History Rekomendasi Pada : {data['date']} ===========\n")
            print("Pilihan Tiket : ")
            print("No. Maskapai\tRute Penerbangan\tKeberangkatan\tPenumpang\t Harga Tiket")
            print("_" * 86)
            print(f"1.  {data['maskapai']}\t{data['asal']} - {data['tujuan']}\t{data['flay']}\t{data['qty']} orang\t\t","Rp. {:3,.0f}".format(int(data['harga'])))
            
            #menampilkan file history hotel berdasarkan date dari looping history hotel
            for query in showHotel:
                if query['date'] == data['date']:
                    print('\nPilihan Hotel : ')
                    print('Nama\t\t Harga')
                    print("_" * 34)
                    print(f"Hotel {query['nama']}\t\tRp. {query['harga']}")

                    #menhitung total bayar
                    ppn = int(data['harga']) * 10/100
                    bayar = ((int(data['qty']) * int(data['harga']) + ppn)) + float(query['harga'].replace(',',''))
                    harga_tiket = "{:3,.0f}".format(int(data['harga']))
                    print("\nTotal Biaya : ")
                    print(f"(({data['qty']}  x {harga_tiket}) + 10%) + Rp.{query['harga']} = ", "Rp. {:3,.2f}\n".format(bayar))
            openFileHotel.close
            
    except IOError:
        print('File', fileHistoryTiket, 'dan', fileHistoryHotel, 'Tidak Ditemukan')
    

again = True
while again:
    #menampilkan menu utama
    print('========= TRAVELU ===========')
    print('1. Cari Rekomendasi Baru')
    print('2. Lihat History Pilihan\n')
    pilih = int(input('Pilih Menu : '))

    #validasi inputan menu
    if pilih == 1:
        tiket()

        #looping fitur rekomendasi
        while again:
            again = input('\nIngin Cari Lagi ? (Y/N) : ')
            if again == 'Y' or again == 'y':
                tiket()
            elif again == 'N' or again == 'n':
                break
            else:
                continue
    elif pilih == 2:
        history()
    else:
        print('Pilihan Menu Tidak Dikenal\n')
        continue
    
    while again:
        loop = input('\nPilih Menu Lain ? (Y/N) : ')
        print()
        #validasi inputan loop
        if loop == 'Y' or loop == 'y':
            again = True
            break
        elif loop == 'N' or loop == 'n':
            print('Terima Kasih')
            again = False
            break 
        else:
            continue
    if again == True:
        continue
    else:
        break